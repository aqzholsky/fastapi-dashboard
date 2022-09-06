import React, {useEffect, useState} from 'react';
import '@trendmicro/react-toggle-switch/dist/react-toggle-switch.css';
import PlayPause from "./PlayPause";
import axios from "axios";
import {useParams} from "react-router-dom";

function Starter() {
    const ROBOT_STATE_API = '/robot_state/';
    const { id } = useParams();
    const [state, setState] = useState({ showPlayButton: true });

    const getRobotState = () => {
        const headers = {
            "Authorization": `Bearer ${localStorage.getItem('jwtToken')}`
        }

        axios.get(ROBOT_STATE_API + `${id}`, {headers: headers})
            .then(res => {
                if (res.data['state'] === 'play'){
                    setState({showPlayButton: true})
                } else if (res.data['state'] === 'stop') {
                    setState({showPlayButton: false})
                }
            }).catch(err=> {
                console.log(err);
            })
    }

    useEffect(() => {
        getRobotState();
    }, []);

    const setRobotState = () => {
        setState({showPlayButton: !showPlayButton});

        const headers = {
            "Authorization": `Bearer ${localStorage.getItem('jwtToken')}`
        }

        const data = {
            robot_id: id,
            state: showPlayButton ? 'stop': 'play',
        }

        console.log(data);

        axios.post(ROBOT_STATE_API, data, {headers: headers})
            .then(res => {
                if (res.data === false) {
                    alert('Вышла неожиданная ошибка');
                }
            }).catch(err=> {
            console.log(err);
        })
    }

    const { showPlayButton } = state

    return (
        <div style={{textAlign: 'right', float: "right"}}>
            <button
                id='play-pause'
                onClick={setRobotState}
                style={{
                    border: "none",
                    backgroundColor: showPlayButton ? "rgb(0, 128, 0, 0.6)" : "rgb(255, 0, 0, 0.8)",
                    boxShadow: "0 0 12px 6px rgba(0,0,0,.2)",
                    cursor: "pointer",
                    height: 40,
                    outline: "none",
                    borderRadius: "100%",
                    width: 40,
                    display: "block",
                    marginLeft: "auto",
                    marginRight: "auto",
                }}
            >
                <PlayPause buttonToShow={showPlayButton} />
            </button>
            <p htmlFor='play-pause' className='mt-2'>Play / Pause</p>
        </div>
    );
}

export default Starter;