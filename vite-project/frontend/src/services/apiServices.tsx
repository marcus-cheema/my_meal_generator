import axios from 'axios';
import { UserFormProps } from '../assets/components/UserInfoForm/UserInfoForm'; // Import UserFormProps

let BASE_URL = 'http://18.191.65.24'; // AWS
// let BASE_URL = 'http://127.0.0.1:8080' // Local

export async function sendMessage(userMessage: string) {
    return axios.post(`${BASE_URL}/api/send_message`, {
      message: userMessage
    })
    .then(function(response) {
      return response;
    })
    .catch(function(error) {
      console.log(error)
    })
}

export async function getBotResponse() {
    return axios.get(`${BASE_URL}/api/bot_response`) // backend URL
      .then(function(response) {
        return response.data.response
      })
      .catch(function(error) {
        console.log(error)
      })
}

export async function getBmrCalculation(formData: UserFormProps) {
  return axios.post(`${BASE_URL}/api/calculate_bmr`, formData)
    .then(function(response) {
      return response;
    })
    .catch(function(error) {
      console.log("Error calculating BMR", error);
    });
}