import React, {useEffect, useState} from 'react';
import { DataGrid } from '@mui/x-data-grid';
import {useParams} from "react-router-dom";
import axios from "axios";

const columns = [
    { field: 'id', headerName: 'ID'},
    { field: 'iin', headerName: 'IIN', width: 200},
    { field: 'full_name', headerName: 'Full name', width: 500 },
    { field: 'status', headerName: 'Status', width: 500},
    {
        field: 'result',
        headerName: 'Result',
        width: 500,
    },
    {
        field: 'service_name',
        headerName: 'Service Name',
        width: 500,
    },
];

function TableReport() {
    const ROBOT_REQUESTS_API = '/request/robot/';
    const { id } = useParams();
    const [requests, setRequests] = useState([]);

    const getMyRequests = () => {
        const headers = {
            "Authorization": `Bearer ${localStorage.getItem('jwtToken')}`
        }

        axios.get(ROBOT_REQUESTS_API + `${id}`, {headers: headers})
            .then(res => {
                let counter = 1;
                let arr = res['data'];
                let requests = [];
                arr.forEach(e => {
                    requests.push({
                        id: counter,
                        iin: e['iin'],
                        full_name: e['last_name'] + ' ' + e['first_name'],
                        status: e['status'],
                        result: e['result'],
                        service_name: e['service_name'],
                    })
                    counter++;
                })
                setRequests(requests);
            }).catch(err=> {
            console.log(err);
        })
    }

    useEffect(() => {
        getMyRequests();
    }, []);

    return (
        <div style={{ height: 500, width: '100%' }}>
            <DataGrid
                rows={requests}
                columns={columns}
            />
        </div>
    );
}

export default TableReport
