// import '../../App.css';
import styles from './InputButton.module.css'
import 'bootstrap/dist/css/bootstrap-grid.min.css'
import { MouseEvent } from 'react'
import '../TextInput/TextInput'

interface UserTextButton {
    handleClick: (e: MouseEvent) => void
}

function UserTextButton(props: UserTextButton) { // have to use hook in order to keep track of and display user messages
    
    return(
        <button 
            type="button" 
            className={`${styles.inputButton} btn`}
            onClick= { (e: MouseEvent) => {
                props.handleClick(e)
            }}
        >Send</button>
    )
}

export default UserTextButton