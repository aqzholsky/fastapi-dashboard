import React, {useEffect, useState} from "react";
import {Doughnut} from "react-chartjs-2";
import {Chart as ChartJs, Tooltip, Title, ArcElement, Legend} from 'chart.js';
import {useParams} from "react-router-dom";
import axios from "axios";
ChartJs.register(
    Tooltip, Title, ArcElement, Legend
);

export default function DoughnutChart({style}) {
    const DAILY_STAT_API = '/request_statistics/daily_requests_by_status/';
    const { id } = useParams();
    const [labels, setLabels] = useState([]);
    const [values, setValues] = useState([]);

    const getDailyStat = () => {
        const headers = {
            "Authorization": `Bearer ${localStorage.getItem('jwtToken')}`
        }

        axios.get(DAILY_STAT_API + `${id}`, {headers: headers})
            .then(res => {
                let arr = res['data'];
                let labels = [];
                let values = [];
                arr.forEach(e => {
                    labels.push(e['status']);
                    values.push(e['count']);
                })
                setLabels(labels);
                setValues(values);
                console.log(res);
            }).catch(err=> {
            console.log(err);
        })
    }

    useEffect(() => {
        getDailyStat();
    }, []);

    const data = {
        labels: labels,
        datasets: [{
            label: 'Daily Statistic',
            data: values,
            backgroundColor: [
                'rgb(255, 99, 132)',
                'rgb(54, 162, 235)',
                'rgb(255, 205, 86)',
                'rgb(255, 35, 160)',
            ],
            hoverOffset: 4,
        }]
    };

    const options = {
        plugins: {
            legend: {
                display: false,
            },
        },
        responsive: true,
        maintainAspectRatio: false,
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero:true
                }
            }]
        }
    };

    return (
        <div style={style}>
            <Doughnut data={data} options={options}/>
        </div>
    )
}