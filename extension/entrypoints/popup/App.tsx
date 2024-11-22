import { useState } from 'react';
import reactLogo from '@/assets/react.svg';
import wxtLogo from '/wxt.svg';
import './App.css';
import { getInfo, findFilledValues_transformerjs, findFilledValues_fastapi } from './requests';

function App() {
  const [text, setText] = useState<string>('');
  const [fields, setFields] = useState(null); // State to store the fields information
  const [response, setResponse] = useState(null); // State to store response from set_fields

  const handleTextareaChange = (event: React.ChangeEvent<HTMLTextAreaElement>) => {
        setText(event.target.value); // Update the state with the current value of the textarea
  };

  const sendMessage = async () => {
    try {
      console.log('Textarea content:', text);

      // Send get_fields message to get the field information
      const fieldInfo = await browser.runtime.sendMessage({ type: 'get_fields' });
      console.log('Field info:', fieldInfo[0].response);
      // setFields(fieldInfo[0].response);
      
      // Create a new dictionary to send back with updated field values
      const updatedFields = await findFilledValues_transformerjs(fieldInfo[0].response);
      // setFields(updatedFields);

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
      <h1>Fill Me In</h1>
      <div className="card">
        <textarea
                value={text}
                onChange={handleTextareaChange}
                placeholder="Type something here..."
                style={{ width: '100%', height: '100px', marginBottom: '10px' }}
        />
        <button onClick={() => sendMessage()}>
            Fill me !
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
