import axios from 'axios';

export async function sendMessage(userMessage: string) {
    console.log("I am being sent a message")
    return axios.post('http://127.0.0.1:8080/api/send_message', {
      message: userMessage
    })
    .then(function(response) {
      console.log("Backend response from POST: ", response.data);
      return response;
    })
    .catch(function(error) {
      console.log(error)
    })
}

export async function getBotResponse() {
    console.log("GET REQUEST")

    return axios.get('http://127.0.0.1:8080/api/bot_response') // backend URL
      .then(function(response) {
        console.log("Backend Message Response from GET: ", response.data.response) // in TS, console.log with Comma and not +
        return response.data.response
      })
      .catch(function(error) {
        console.log(error)
      }
    )
}

// useEffect(() => {
//     getBotResponse();
//   }, []);

// useEffect(() => {
//     sendMessage("Hi bot! I am the USER")
//   }, []); // runs once