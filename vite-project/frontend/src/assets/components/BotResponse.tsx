import '../../App.css';
import 'bootstrap/dist/css/bootstrap-grid.min.css'

interface BotResponseProps {
    responseMessage: string;
}

function BotResponse(props: BotResponseProps) {
    return (
        <div className="card bot-response">
            <div className="card-body"> {props.responseMessage} </div>
        </div>
    )
}

export default BotResponse