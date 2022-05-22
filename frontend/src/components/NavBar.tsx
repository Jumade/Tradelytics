import {Container, Nav, Navbar, NavDropdown} from "react-bootstrap";
import { useRecoilValue } from "recoil";
import { useAccountActions } from "../actions/AccountActions";
import { authUserAtom } from '../state/AccountState';



function NavBar() {
    let userAuth = useRecoilValue(authUserAtom);
    
    const accountActions = useAccountActions();

    return (
        <Navbar bg="dark" variant="dark">
            <Container>
                <Navbar.Brand href="/">Tradelytics</Navbar.Brand>
                <Nav className="me-auto">
                    <Nav.Link href="/">Positions</Nav.Link>
                </Nav>
                
                {userAuth
                    ? <Navbar.Text>Signed in</Navbar.Text>
                    : <Navbar.Text className="justify-content-end">You are not logged in.</Navbar.Text>
                }
                {userAuth && 
                    <NavDropdown title="Account" id="nav-dropdown" >
                        <NavDropdown.Item eventKey="4.1" onClick={() => { accountActions.signout(); }}>Logout</NavDropdown.Item>
                        <NavDropdown.Divider />
                        <NavDropdown.Item href="settings" eventKey="4.2">API Settings</NavDropdown.Item>
                    </NavDropdown> 
                }
            </Container>
        </Navbar>

    );
}


export default NavBar;
  