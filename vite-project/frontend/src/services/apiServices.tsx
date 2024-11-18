import axios from 'axios';
import { UserFormProps } from '../assets/components/UserInfoForm/UserInfoForm'; // Import UserFormProps

export async function sendMessage(userMessage: string) {
    return axios.post('http://18.191.65.24/api/send_message', {
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
    return axios.get('http://18.191.65.24/api/bot_response') // backend URL
      .then(function(response) {
        return response.data.response
      })
      .catch(function(error) {
        console.log(error)
      })
}

export async function getBmrCalculation(formData: UserFormProps) {
  return axios.post('http://18.191.65.24/api/calculate_bmr', formData)
    .then(function(response) {
      return response;
    })
    .catch(function(error) {
      console.log("Error calculating BMR", error);
    });
}