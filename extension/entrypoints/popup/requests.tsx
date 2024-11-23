import { pipeline } from '@huggingface/transformers';

const classifier = await pipeline('zero-shot-classification', 'Xenova/nli-deberta-v3-xsmall');


async function getInfo(field_name, label_list, data) {
    const output = await classifier(field_name, label_list, { multi_label: false });
    const choice = output.labels[0];
    if (choice === "other") {
        console.log("NO MATCH", field_name);
        return null;
    } else {
        console.log("MATCH", field_name, choice, data[choice]);
        const choice_value = data[choice];
        const choice_score = output.scores[0];
        //const res = `${choice_value} -- ${choice_score}`
        const res = choice_value
        return res;
    }
}

async function mapFields(extractedFields, data) {
    const label_list = Object.keys(data);
    label_list.push("other");
    console.log("LABELS LIST", label_list);
    const filling_dict = {};

    for (const field of extractedFields) {
      let value = null;

      if (field.type === "text" || field.type === "textarea" || field.type === "email") {
        value = await getInfo(field.name, label_list, data); // Assume getInfo is an async function
      } else {
        console.log("Field type not taken into account:", field.type);
      }

      // Add the value to dict if it's not null
      if (value !== null) {
        filling_dict[field.name] = value;
      }
    }

    console.log("FILLING DICT", filling_dict);

    return filling_dict;
}

export async function findFilledValues_transformerjs(extractedFields) {
    // HARDCODED Version
    const user_data = {
        "name": "John Doe bro",
        "email": "johndoebro@gmail.com",
        "company": "johndoecorp",
        "phone number": "+331234567890",
        "postal address": "1 rue du paradis, 75007"
    };
    const filling_dict = await mapFields(extractedFields, user_data);
    return filling_dict;
}

async function getUserData(text, extractedFields) {
    console.log("EXTRACTEDFIELDS", extractedFields);
    try {
        const dict = {};

        extractedFields.forEach(inputField => {
          if (inputField.type === 'text' || inputField.type === 'textarea' || inputField.type === 'email') {
            dict[inputField.name] = "<value>";
            console.log("No Skip:", inputField.name, inputField.type);
          } else {
            console.log("Skip:", inputField.name, inputField.type);
          }
        });
        const payload = JSON.stringify({
            "user_info": text,
            "json_data": dict
        });
        console.log(payload);
        const url = 'http://localhost:8080/form';

        // Make the POST request using fetch
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json' // Specify JSON format
            },
            body: payload // Stringify the extractedFields object
        });

        // Check if the response is OK (status in range 200-299)
        if (!response.ok) {
            console.log(response.json());
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        // Parse and return the response as JSON
        const data = await response.json();
        console.log("Response from server:", data);
        return data;
    } catch (error) {
        console.error("Error sending POST request:", error);
        throw error;
    }
}

export async function findFilledValues_fastapi(text, extractedFields) {
    const user_data = await getUserData(text, extractedFields);
    const filling_dict = await mapFields(extractedFields, user_data);
    return filling_dict;
}
