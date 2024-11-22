import ollama from 'ollama'

function extractFormData() {
  // Get all form elements inside the form
  const form = document.querySelector('#application-form');
  const inputs = form.querySelectorAll('input, select, textarea, button');
  
  // Initialize an array to hold the extracted data
  let formData = [];

  // Loop through each input element and collect required details
  inputs.forEach(input => {
    const name = input.name || '';
    const label = input.closest('label') ? input.closest('label').querySelector('.application-label')?.textContent.trim() : '';
    const type = input.type || '';
    const id = input.id || '';
    
    // Only add the data if the name is not empty
    if (name) {
      formData.push({ name, label, type, id });
    }
  });

  return formData;
}

function setFormData(formData) {
  // Iterate over each field in the form data
  Object.keys(formData).forEach(key => {
    // Get the value for the current field
    const value = formData[key];
    console.log(key, value);
    
    // Handle different input types (radio buttons, checkboxes, select elements, etc.)
    const field = document.querySelector(`[name="${key}"]`);
    console.log(field);
    
    if (!field) return; // If the field doesn't exist, skip it

    // Check the type of the field and set the value accordingly
    if (field.type === 'radio') {
      // For radio buttons, set the checked attribute
      if (field.value === value) {
        field.checked = true;
      }
    } else if (field.type === 'checkbox') {
      // For checkboxes, check/uncheck based on value (assuming boolean values)
      field.checked = !!value;
    } else if (field.type === 'select-one') {
      // For select dropdowns, set the selected option
      Array.from(field.options).forEach(option => {
        if (option.value === value) {
          option.selected = true;
        }
      });
    } else if (field.type === 'select-multiple') {
      // For multiple select dropdowns, select options based on value array
      const selectedValues = Array.isArray(value) ? value : [value];
      Array.from(field.options).forEach(option => {
        option.selected = selectedValues.includes(option.value);
      });
    } else if (field.type === "text" || field.type === "textarea" || field.type == "email") {
      // For other input types, set the value directly
      field.value = value;
    } else {
      console.log("Field type not taken into account:", field.type);
    }
  });
}


export default defineContentScript({
  matches: ['*://*.google.com/*', '*://*.lever.co/*', '*://*.lever.co/*'],
  main() {
    console.log('Hello content.');
    // browser.runtime.onMessage.addListener(async (message) => {
    //   console.log("Content script recieved message:", message);
    //     const inputs = document.querySelectorAll('input[type="text"]');
    //       inputs.forEach((input) => {
    //           input.value = "PLACEHOLDER";
    //   });
    //   return Math.random();
    // });
    browser.runtime.onMessage.addListener(async (message) => {
      console.log("Content script received message:", message);

      if (message.type === "get_fields") {
        const fields = extractFormData();
        console.log("Fields found:", fields);
        return fields; // Return the list of fields
      } else if (message.type === "set_fields" && message.content) {
        // Set input field values based on message.content
        const { content } = message;
        console.log("Updated fields", content);
        setFormData(content);
        return { success: true };
      } else {
        console.warn("Unknown message type or missing content");
        return { error: "Invalid message type or content" };
      }
    });
  },
});
