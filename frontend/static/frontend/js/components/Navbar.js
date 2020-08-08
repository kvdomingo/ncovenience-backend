import React from 'react';
import {
    MDBNavbar as Navbar,
    MDBNavbarBrand as NavbarBrand,
    MDBNavbarNav as NavbarNav,
    MDBNavItem as NavItem,
    MDBNavLink as NavLink,
    MDBNavbarToggler as NavbarToggler,
    MDBCollapse as Collapse,
} from 'mdbreact';


export default class Navigation extends React.Component {
    state = {
        isOpen: false,
    }

    toggleCollapse = () => {
        this.setState(prevState => ({ isOpen: !prevState.isOpen }));
    }

    render() {
        return (
            <Navbar dark expand='lg' className='bg-dark' style={{ boxShadow: 'none' }}>
                <NavbarBrand>
                    <NavLink to='/' className='text-white'>
                        <span style={{ fontVariant: 'small-caps' }}>ncovenience</span>: COVID-19 PH Tracker
                    </NavLink>
                </NavbarBrand>
                <NavbarToggler onClick={this.toggleCollapse} />
                <Collapse isOpen={this.state.isOpen} navbar>
                    <NavbarNav left>
                        <NavItem>
                            <NavLink to='/'>Home</NavLink>
                        </NavItem>
                        <NavItem>
                            <NavLink to='docs'>API</NavLink>
                        </NavItem>
                    </NavbarNav>
                </Collapse>
            </Navbar>
        );
    }
}
