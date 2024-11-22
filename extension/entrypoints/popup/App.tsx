import { useState } from 'react';
import reactLogo from '@/assets/react.svg';
import wxtLogo from '/wxt.svg';
import './App.css';


function findFilledValues(extractedFields) {
    // const data = extractedFields.response.reduce((acc, field) => {
    //     // Example: Modify value (you can customize this as needed)
    //     acc[field.name] = field.name; // Set the value as uppercase ID
    //     return acc;
    //   }, {});

    const data = {
        "name": "John Doe",
        "email": "johndoe@gmail.com",
        "phone": "+33783926745",
        "location": "Paris"
    };
    return data;
}

function App() {
  const [count, setCount] = useState(0);
  const [fields, setFields] = useState(null); // State to store the fields information
  const [response, setResponse] = useState(null); // State to store response from set_fields

  const sendMessage = async () => {
    try {
      // Send get_fields message to get the field information
      const fieldInfo = await browser.runtime.sendMessage({ type: 'get_fields' });
      console.log('Field info:', fieldInfo[0].response);
      
      // Create a new dictionary to send back with updated field values
      const updatedFields = findFilledValues(fieldInfo[0].response);
      setFields(updatedFields);

      // Send set_fields message with updated fields
      const updateResponse = await browser.runtime.sendMessage({
        type: 'set_fields',
        content: updatedFields,
      });
      console.log('Set fields response:', updateResponse);

      // Store the response from set_fields to display later
      setResponse(updateResponse);
    } catch (error) {
      console.error('Error sending message:', error);
    }
  };

  return (
    <>
      <div>
        <a href="https://wxt.dev" target="_blank">
          <img src={wxtLogo} className="logo" alt="WXT logo" />
        </a>
        <a href="https://react.dev" target="_blank">
          <img src={reactLogo} className="logo react" alt="React logo" />
        </a>
      </div>
      <h1>WXT + React</h1>
      <div className="card">
        <button onClick={() => setCount((count) => count + 1)}>
          count is {count}
        </button>
        <button onClick={() => sendMessage()}>
        send message
        </button>
        <p>
          Edit <code>src/App.tsx</code> and save to test HMR
        </p>
        {/* Display the fields info */}
        <div>
          {fields ? (
            <pre className="fields-info">{JSON.stringify(fields, null, 2)}</pre>
          ) : (
            <p>No field info yet.</p>
          )}
        </div>

        {/* Display the response of set_fields */}
        <div>
          {response ? (
            <pre className="response-display">{JSON.stringify(response, null, 2)}</pre>
          ) : (
            <p>No response yet from set_fields.</p>
          )}
        </div>
      </div>
      <p className="read-the-docs">
        Click on the WXT and React logos to learn more
      </p>
    </>
  );
}

export default App;
