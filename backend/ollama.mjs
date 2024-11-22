// Dowload ollama
//          https://ollama.com/download
// run ->   
//        ollama pull llama3.2:1b
//        npm install --save ollama
//       node kiwi.mjs
import ollama from 'ollama'
import fs from 'fs'

// load message from a txt file
const message = fs.readFileSync('prompt.txt', 'utf8')

const response = await ollama.chat({
  model: 'llama3.2:1b',
  format: 'json',
  messages: [{ role: 'user', content: message}],
})
// ⚠️ Ceci peut prendre beaucoup de temps car on attend la réponse complète
console.log(response.message.content)
