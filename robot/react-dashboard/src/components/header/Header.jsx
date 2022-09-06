import React from 'react';
import {
    MDBNavbar,
    MDBNavbarNav,
    MDBNavbarItem,
    MDBNavbarLink,
    MDBNavbarToggler,
    MDBContainer,
    MDBIcon,
    MDBCardImage
} from 'mdb-react-ui-kit';

import {MDBFormInline} from "mdbreact";

import robot_logo from "../../assets/robot_logo.webp";
import "./Header.css";


function Header() {
    const userName = localStorage.getItem('username');

    return (
        <header>
            <MDBNavbar expand='lg' className="header_style" light>
                <MDBContainer fluid>
                    <MDBNavbarToggler
                        aria-controls='navbarExample01'
                        aria-expanded='false'
                        aria-label='Toggle navigation'
                    >
                        <MDBIcon fas icon='bars' />
                    </MDBNavbarToggler>
                    <div className='collapse navbar-collapse'>
                        <MDBNavbarNav className='mb-2 mb-lg-0'>
                            <MDBNavbarItem active>
                                <MDBNavbarLink aria-current='page' href='/'>
                                    <MDBCardImage src={robot_logo} height='50px' width='50px'/>
                                </MDBNavbarLink>
                            </MDBNavbarItem>
                            <MDBNavbarItem className="header_li" style={{marginLeft: '3%'}}>
                                <MDBNavbarLink className="header_link" href='/'>Robots</MDBNavbarLink>
                            </MDBNavbarItem>
                        </MDBNavbarNav>
                    </div>
                    <div className='navbar-nav-scroll'>
                        <MDBNavbarNav className='mb-2 mb-lg-0'>
                            {/*<MDBNavbarItem>*/}
                            {/*    <div className="md-form my-0">*/}
                            {/*        <input className="form-control mr-sm-2" type="text" placeholder="Search" aria-label="Search" />*/}
                            {/*    </div>*/}
                            {/*</MDBNavbarItem>*/}
                            <MDBNavbarItem style={{marginRight: '3%'}}>
                                <MDBNavbarLink className="header_link" href='#'>{userName}</MDBNavbarLink>
                            </MDBNavbarItem>
                        </MDBNavbarNav>
                    </div>
                </MDBContainer>
            </MDBNavbar>
            <br />
        </header>
    );
}

export default Header