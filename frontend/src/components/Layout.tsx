import {Outlet} from "react-router-dom";
import NavBar from "./NavBar";

function Layout() {
    return (
        <div>
            <header className="App-header">
                <NavBar />
            </header>
            <main role="main" className="container">
                <Outlet />
            </main>

        </div>
    );
}

export default Layout;



