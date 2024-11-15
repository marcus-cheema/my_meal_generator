// import '../../App.css';
import styles from './BotResponse.module.css'
import 'bootstrap/dist/css/bootstrap-grid.min.css'

interface BotResponseProps {
    responseMessage: string;
}

function BotResponse(props: BotResponseProps) {
    let formattedResponse = props.responseMessage.split('\n').map((line, index) => (
        <span key={index}>
            {line}
            <br />
        </span>
    ));
    return (
        <div className={`${styles.botResponse} card`}>
            <div className="card-body"> {formattedResponse} </div>
        </div>
    )
}

export default BotResponse