import React from "react";
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faPlay, faStop } from '@fortawesome/free-solid-svg-icons'

const PlayPause = React.memo(function PlayPause({ buttonToShow }) {

    const faStyle = {
        width: '23px',
        height: '23px'
    }

    return (
        <div >
            {buttonToShow
                ? <FontAwesomeIcon className='file_upload_icon' icon={faPlay} style={faStyle}/>
                : <FontAwesomeIcon className='file_upload_icon' icon={faStop} style={faStyle}/>
            }
        </div>

    );
});
export default PlayPause;
