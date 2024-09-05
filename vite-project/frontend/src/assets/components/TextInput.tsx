import 'bootstrap/dist/css/bootstrap.min.css'
import '../../App.css'
import { KeyboardEvent } from 'react'

interface TextInputProps {
    userMessage: string;
    setUserMessage: (message: string) => void;
    onKeyDown: (e: KeyboardEvent) => void;
}


function TextInput(props: TextInputProps) {

    // let [userMessage, setUserMessage] = useState('')

    return (
        <input 
            className="form-control form-control-lg text-input"
            id="textInput" 
            type="text" 
            placeholder="Ask a question"
            value={props.userMessage}
            onChange={ (e) => { // in the event that the User changes the input, the event will set the userMessage to current message.
                props.setUserMessage(e.target.value)
            }}
            onKeyDown={props.onKeyDown}
        />
    )
}

export default TextInput