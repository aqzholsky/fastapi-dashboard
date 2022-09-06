import React, {useState, useEffect} from 'react';
import { styled } from '@mui/material/styles';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell, { tableCellClasses } from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';
import Header from "../header/Header";
import axios from "axios";

const StyledTableCell = styled(TableCell)(({ theme }) => ({
  [`&.${tableCellClasses.head}`]: {
    backgroundColor: theme.palette.common.black,
    color: theme.palette.common.white,
  },
  [`&.${tableCellClasses.body}`]: {
    fontSize: 14,
  },
}));


export default function Main() {
    const MY_ROBOTS_API = '/robot/';
    const [robots, setRobots] = useState([]);

    const getMyRobots = () => {
        const headers = {
            "Authorization": `Bearer ${localStorage.getItem('jwtToken')}`
        }

        axios.get(MY_ROBOTS_API, {headers: headers})
            .then(res => {
                let arr = res['data'];
                let robots = [];
                arr.forEach(e => {
                    robots.push({
                        id: e['id'],
                        name: e['name'],
                        server_address: e['server_address'],
                        state: e['state'],
                        start_time: e['start_time'],
                        end_time: e['end_time'],
                    })
                })
                setRobots(robots);
            }).catch(err=> {
            console.log(err);
        })
    }

    useEffect(() => {
        getMyRobots();
    }, []);

    return (
      <div className="container-fluid">
        <Header />
        <div className="container">
          <TableContainer component={Paper} sx={{ width: '100%' }}>
          <Table>
            <TableHead>
              <TableRow>
                  <StyledTableCell>Robot</StyledTableCell>
                  <StyledTableCell align="right">Server Address</StyledTableCell>
                  <StyledTableCell align="right">State</StyledTableCell>
                  <StyledTableCell align="right">Start Time</StyledTableCell>
                  <StyledTableCell align="right">End Time</StyledTableCell>
                  <StyledTableCell align="right">More Details</StyledTableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {robots.map((robot) => (
                <TableRow key={robot.name}>
                  <TableCell component="th" scope="row">{robot.name}</TableCell>
                  <TableCell align="right">{robot.server_address}</TableCell>
                  <TableCell align="right">{robot.state}</TableCell>
                  <TableCell align="right">{robot.start_time}</TableCell>
                  <TableCell align="right">{robot.end_time}</TableCell>
                  <TableCell align="right"><a href={`detail/${robot.id}`} style={{color: 'black'}}>Detail</a></TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
        </div>
      </div>
  );
}
