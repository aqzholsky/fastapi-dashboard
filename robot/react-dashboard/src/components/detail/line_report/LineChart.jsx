import React, {useEffect, useState} from "react";
import ReactApexChart from 'react-apexcharts'
import {useParams} from "react-router-dom";
import axios from "axios";

function compare(a, b) {
    const date1 = a.date.split('.').reverse().join('');
    const date2 = b.date.split('.').reverse().join('');
    return date1.localeCompare(date2);
}


function LineChart () {
    const MONTHLY_STAT_API = '/request_statistics/daily_requests_of_last_month/';
    const { id } = useParams();
    const [yAxisData, setYAxisData] = useState([]);
    const [xAxisData, setXAxisData] = useState([]);


    const getMonthlyStat = () => {
        const headers = {
            "Authorization": `Bearer ${localStorage.getItem('jwtToken')}`
        }

        axios.get(MONTHLY_STAT_API + `${id}`, {headers: headers})
            .then(res => {
                let arr = res['data'];
                arr.sort(compare)
                let yAxisData = [];
                let xAxisData = [];
                arr.forEach(e => {
                    yAxisData.push(e['count']);
                    xAxisData.push(e['date']);
                })
                setYAxisData(yAxisData)
                setXAxisData(xAxisData);
            }).catch(err=> {
            console.log(err);
        })
    }

    useEffect(() => {
        getMonthlyStat();
    }, []);


    const series = [{
        name: "Desktops",
        data: yAxisData
    }]
    const options = {
        chart: {
            height: 350,
            type: 'line',
            zoom: {
                enabled: false
            }
        },
        dataLabels: {
            enabled: false
        },
        stroke: {
            curve: 'straight'
        },
        title: {
            text: 'Robot Requests',
            align: 'left'
        },
        grid: {
            row: {
                colors: ['#f3f3f3', 'transparent'], // takes an array which will be repeated on columns
                opacity: 0.5
            },
        },
        xaxis: {
            categories: xAxisData,
        }
    }

    return (
        <div id="chart">
            <ReactApexChart options={options} series={series} type="line" height={500} />
        </div>
    );
}

export default LineChart
    