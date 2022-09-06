import React, {useEffect, useState} from 'react';
import { styled } from '@mui/material/styles';
import Box from '@mui/material/Box';
import Paper from '@mui/material/Paper';
import Grid from '@mui/material/Grid';
import 'bootstrap/dist/css/bootstrap.min.css';

import DoughnutChart from './doughnut_report/DoughnutChart';
import LineChart from "./line_report/LineChart";
import TableReport from "./table_report/TableReport";
import Header from "../header/Header";
import UploadModal from "./file_uploader/Upload";
import axios from "axios";
import {useParams} from "react-router-dom";
import Starter from "./starter/Starter";


const Item = styled(Paper)(({ theme }) => ({
    backgroundColor: theme.palette.mode === 'dark' ? '#1A2027' : '#fff',
    ...theme.typography.body2,
    padding: theme.spacing(1),
    textAlign: 'center',
    color: theme.palette.text.secondary,
}));


export default function Detail() {
    const MY_ROBOT_API = '/robot/';
    const { id } = useParams();
    const [robot, setRobot] = useState({});

    const getMyRobot = () => {
        const headers = {
            "Authorization": `Bearer ${localStorage.getItem('jwtToken')}`
        }

        axios.get(MY_ROBOT_API, {headers: headers})
            .then(res => {}).catch(err=> {
            console.log(err);
        })
    }

    useEffect(() => {
        getMyRobot();
    }, []);


    return (
      <div className="container-fluid">
          <Header />
          <Grid container spacing={2}>
              <Grid item xs={10}>
              </Grid>
              <Grid item xs={2}>
                  <Starter />
                  <UploadModal/>
              </Grid>
          </Grid>
          <Box sx={{ flexGrow: 1 }}>
              <Grid container spacing={2}>
                  <Grid item xs={4}>
                      <Item><DoughnutChart style={{height: 515}}/></Item>
                  </Grid>
                  <Grid item xs={8}>
                      <Item><LineChart/></Item>
                  </Grid>
                  <Grid item xs={12}>
                      <Item><TableReport /></Item>
                  </Grid>
              </Grid>
          </Box>
      </div>
  )
}