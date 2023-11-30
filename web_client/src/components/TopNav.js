import { Link } from "react-router-dom";
import logo from '../assets/logo.png'
import Hamburger from "./svg/Hamburger";
import { useState } from "react";
import Xbutton from "./svg/Xbutton";

function TopNav(props) {
    function handleMobileMenu(event) {
        setMobileVisible(!mobileVisible);
        
    }

    const [mobileVisible, setMobileVisible] = useState(false);

    return (
        <div className="header-container">
            <header>
                <nav>
                <div className="logo-container">
                <Link to="/"><img src={logo} className='small-logo' alt="Logo of the website" /></Link>
                </div>
                    <div className="hamburger-container">
                        <div className={mobileVisible ? "invisible" : "visible"} onClick={() => {handleMobileMenu()}}>
                            <Hamburger/>
                        </div>
                        <div className={mobileVisible ? "visible" : "invisible"} onClick={() => {handleMobileMenu()}}>
                            <Xbutton/>
                        </div>
                    </div>
                    <div className={mobileVisible ? "nav-list-container visible" : "nav-list-container invisible"}>
                    <ul>
                        <li className={"menu-item " + ((props.activePage === "/strona-glowna") ? "active" : "")}>
                            <Link to="/">Strona główna</Link>
                        </li>
                        <li className={"menu-item " + ((props.activePage === "/predykcja") ? "active" : "")}>
                            <Link to="/predykcja">Predykcja</Link>
                        </li>
                        <li className={"menu-item " + ((props.activePage === "/obserwacje") ? "active" : "")}>
                            <Link to="/obserwacje">Obserwacje</Link>
                        </li>
                        <li className={"menu-item " + ((props.activePage === "/analiza") ? "active" : "")}>
                            <Link to="/analiza">Analiza</Link>
                        </li>
                        <li className={"menu-item " + ((props.activePage === "/o-projekcie") ? "active" : "")}>
                            <Link to="/o-projekcie">O projekcie</Link>
                        </li>
                    </ul>
                    </div>
                </nav>
            </header>
        </div>
    );
}

export default TopNav;