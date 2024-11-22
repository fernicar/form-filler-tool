// Dowload ollama
//          https://ollama.com/download
// run ->   
//        ollama pull llama3.2:1b
//        npm install --save ollama
//       node kiwi.mjs


import ollama from 'ollama'

const response = await ollama.chat({
  model: 'llama3.2:1b',
  messages: [{ role: 'user', content: 'You are an intelligent scheduling assistant. Your job is to convert short, informal instructions into polite and professional messages that can be sent directly to the recipient to request a service or schedule an appointment. Analyze the input to extract key details:    Time and date of the meeting or service. Recipient type (e.g., barber, doctor, restaurant, etc.).           Service requested (if provided).    Construct a polite and concise message based on this information. The tone should be courteous and professional'}],
})
// ⚠️ Ceci peut prendre beaucoup de temps car on attend la réponse complète
console.log(response.message.content)
