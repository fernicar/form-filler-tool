import { useState } from 'react';
import reactLogo from '@/assets/react.svg';
import wxtLogo from '/icon.svg';
import './App.css';
import { getInfo, findFilledValues_transformerjs, findFilledValues_fastapi } from './requests';
import { storage } from 'wxt/storage';

function App() {
  const [text, setText] = useState<string>(null);
  const [fields, setFields] = useState(null); // State to store the fields information
  const [response, setResponse] = useState(null); // State to store response from set_fields

  const handleTextareaChange = (event: React.ChangeEvent<HTMLTextAreaElement>) => {
        const description = event.target.value;
        setText(description); // Update the state with the current value of the textarea
        storage.setItem('local:description', description);
  };

  useEffect(() => {
    const fetchDescription = async () => {
      try {
        const description = await storage.getItem('local:description');
        setText(description); // Set the fetched value to the state
      } catch (error) {
        console.error('Failed to fetch description:', error);
      }
    };

    fetchDescription(); // Call the async function inside useEffect
  }, []);

  const sendMessage = async () => {
    try {
      console.log('Textarea content:', text);

      // Send get_fields message to get the field information
      const fieldInfo = await browser.runtime.sendMessage({ type: 'get_fields' });
      console.log('Field info:', fieldInfo[0].response);
      // setFields(fieldInfo[0].response);
      
      // Create a new dictionary to send back with updated field values
      const updatedFields2 = await findFilledValues_fastapi(text, fieldInfo[0].response);
      console.log("UPDATED FIELDS", updatedFields2);

      // const updatedFields = await findFilledValues_transformerjs(fieldInfo[0].response);
      // setFields(updatedFields);

      // Send set_fields message with updated fields
      const updateResponse = await browser.runtime.sendMessage({
        type: 'set_fields',
        content: updatedFields2,
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
        <a>
          <img src={wxtLogo} className="logo" alt="Logo" />
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
      </div>
      <p className="read-the-docs">
        Enter your details once, and save time for the moments that matter.
      </p>
    </>
  );
}

export default App;
