import { pipeline } from '@huggingface/transformers';

const classifier = await pipeline('zero-shot-classification', 'Xenova/nli-deberta-v3-xsmall');
const user_data = {
    "name": "John Doe bro",
    "email": "johndoebro@gmail.com",
    "company": "johndoecorp",
    "phone number": "+331234567890",
    "postal address": "1 rue du paradis, 75007"
};
const labels = Object.keys(user_data);
labels.push("other");


async function getInfo(field_name) {
    const output = await classifier(field_name, labels, { multi_label: false });
    const choice = output.labels[0];
    if (choice === "other") {
        console.log("NO MATCH", field_name);
        return null;
    } else {
        console.log("MATCH", field_name, choice, user_data[choice]);
        const choice_value = user_data[choice];
        const choice_score = output.scores[0];
        const res = `${choice_value} -- ${choice_score}`
        return res;
    }
}

export async function findFilledValues_transformerjs(extractedFields) {
    console.log("EXTRACTEDFIELDS", extractedFields);

    const filling_dict = {};

    for (const field of extractedFields) {
      let value = null;

      if (field.type === "email") {
        value = user_data["email"];
      } else if (field.type === "text" || field.type === "textarea") {
        value = await getInfo(field.name); // Assume getInfo is an async function
      } else {
        console.log("Field type not taken into account:", field.type);
      }

      // Add the value to dict if it's not null
      if (value !== null) {
        filling_dict[field.name] = value;
      }
    }

    console.log("FILLING DICT", filling_dict);

    // const filling_dict = {
    //     "name": "John Doe",
    //     "email": "johndoe@gmail.com",
    //     "phone": "+33783926745",
    //     "location": "Paris"
    // };
    
    return filling_dict;
}

export async function findFilledValues_fastapi(extractedFields) {
    console.log("EXTRACTEDFIELDS", extractedFields);
    try {
        // Construct the URL
        const url = 'http://localhost:8080/';

        // Make the POST request using fetch
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json' // Specify JSON format
            },
            body: JSON.stringify(extractedFields) // Stringify the extractedFields object
        });

        // Check if the response is OK (status in range 200-299)
        if (!response.ok) {
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

