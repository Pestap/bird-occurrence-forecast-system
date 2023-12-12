import {Link} from "react-router-dom";
import TopNav from "../components/TopNav";
import heroVideo from '../assets/herovideo.mp4'
import heroVideoPoster from '../assets/herovideoposter.png'

function MainPage() {
    return (
        <div>
            <TopNav activePage="/strona-glowna"/>
            <div className="main-container">
                <div className="main-page-hero">
                    <video autoPlay poster={heroVideoPoster} loop muted playsInline>
                        <source src={heroVideo} type="video/mp4"/>
                        <img alt="Wideo - plakat" src={heroVideoPoster}/>
                    </video>
                    <div className="hero-text-container">
                        <span className="hero-text">System do predykcji występowania ptaków </span>
                        <span className="hero-text small">Projekt realizowany jest w ramach pracy inżynierskiej na Wydziale Elektroniki, Telekomunikacji i Informatyki Politechniki Gdańskiej. </span>
                        <Link to="/predykcja">
                            <button>Sprawdź</button>
                        </Link>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default MainPage;