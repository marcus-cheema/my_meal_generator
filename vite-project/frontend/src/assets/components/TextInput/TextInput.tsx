import 'bootstrap/dist/css/bootstrap.min.css'
import styles from './TextInput.module.css'
// import '../../App.css'
import { KeyboardEvent } from 'react'
import TextareaAutosize from 'react-textarea-autosize';


interface TextInputProps {
    userMessage: string;
    setUserMessage: (message: string) => void;
    onKeyDown: (e: KeyboardEvent) => void;
}

function TextInput(props: TextInputProps) {

    return (
        <TextareaAutosize
            className={`${styles.textInput} form-control form-control-lg`}
            id="textInput" 
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