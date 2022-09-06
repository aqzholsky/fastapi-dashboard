import React, {useState} from 'react';
import Backdrop from '@mui/material/Backdrop';
import Box from '@mui/material/Box';
import Modal from '@mui/material/Modal';
import Fade from '@mui/material/Fade';
import Button from '@mui/material/Button';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faArrowUpFromBracket, faFileUpload } from '@fortawesome/free-solid-svg-icons'
import 'bootstrap/dist/js/bootstrap.bundle';
import 'jquery/dist/jquery.min';
import "./Upload.css";
import axios from "axios";
import {useParams} from "react-router-dom";
import { useNavigate } from 'react-router-dom';

const style = {
    position: 'absolute',
    top: '50%',
    left: '50%',
    transform: 'translate(-50%, -50%)',
    width: 600,
    height: 400,
    bgcolor: 'background.paper',
    border: '2px solid #000',
    boxShadow: 24,
    p: 4,
    alignItems: 'center',
};

export default function UploadModal() {
    const UPLOAD_FILE_API = '/request/bulk_create';
    const { id } = useParams();
    const navigate = useNavigate();
    const [open, setOpen] = React.useState(false);
    const [selectedFile, setSelectedFile] = useState();
    const handleOpen = () => setOpen(true);
    const handleClose = () => setOpen(false);
    const [fileName, setFileName] = React.useState('file_uploader excel or csv file')

    const handleUploadFile = (event) => {
        setSelectedFile(event.target.files[0]);
        setFileName('Вы загрузили: ' + event.target.files[0].name)
    };

    const postUploadFile = (event) => {
        handleClose()

        const headers = {
            "Authorization": `Bearer ${localStorage.getItem('jwtToken')}`,
            "Content-Type": 'multipart/form-data',
        }

        const formData = new FormData();
        formData.append('file', selectedFile);

        axios.post(UPLOAD_FILE_API + `?robot_id=${id}`, formData, {headers: headers})
            .then(res => {
                alert('Успешно');
                console.log(res);
            }).catch(err=> {
                if (err.response.request.status === 400 || err.response.request.status === 415){
                    alert(err.response.data['detail']);
                }
                else{
                    alert('Error');
                }
            console.log(err);
        })

        setFileName('file_uploader excel or csv file');

    }


    return (
        <div style={{textAlign: "center"}}>
            <FontAwesomeIcon
                id='fileUploadIcon'
                icon={faFileUpload}
                onClick={handleOpen}
                style={{
                     boxShadow: "0 0 12px 12px transparent",
                     cursor: "pointer",
                     display: "block",
                     marginLeft: "auto",
                     marginRight: "auto",
                     width: '40px',
                     height: '40px',
                 }} />
            <p htmlFor='fileUploadIcon' className='mt-2'>Upload New Requests</p>
            <Modal
                aria-labelledby="transition-modal-title"
                aria-describedby="transition-modal-description"
                open={open}
                onClose={handleClose}
                closeAfterTransition
                BackdropComponent={Backdrop}
                BackdropProps={{
                    timeout: 500,
                }}
            >
                <Fade in={open}>
                    <Box sx={style}>
                        <div className="file-drop-area">
                            <FontAwesomeIcon className='file_upload_icon' icon={faArrowUpFromBracket} />
                            <span className="file-message">{fileName}</span>
                            <input className="file-input" type="file" accept='.xlsx, .csv' onChange={handleUploadFile}/>
                        </div>
                        <div className="file-send-area">
                            <button className='btn btn-secondary file_upload_btn' type='submit' onClick={postUploadFile}>Send</button>
                        </div>
                    </Box>
                </Fade>
            </Modal>
        </div>
    );
}
