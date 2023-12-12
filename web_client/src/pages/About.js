import TopNav from "../components/TopNav";
import aboutImg from '../assets/about_img_1.jpg'
import {Link, useLocation} from "react-router-dom";

function About() {
    return (
        <div>
            <TopNav activePage={useLocation().pathname}/>
            <div className="main-container about-page">
                <div className="article-container">
                    <article>
                        <img src={aboutImg} alt="kingfisher"/>
                        <h1>O projekcie</h1>
                        <p>Projekt realizowany jest w ramach pracy inżynierskiej na Wydziale Elektroniki, Telekomunikacji i Informatyki Politechniki Gdańskiej.</p>
                        <p>Kod źródłowy projektu można zobaczyć w repozytorimu na platformie Github - <Link to="https://github.com/Pestap/bird-occurrence-forecast-system">link</Link></p>
                        <p>Poniżej znajdują się filmy demonstracyjne przedstawiające przykładowe wykorzystanie funkcjonalności oferowanych przez podstrony Predykcja, Obserwacje i Analiza:</p>
                        <h2>Zakładka Analiza</h2>
                        <iframe className={"yt-video"} width="560" height="315" src="https://www.youtube.com/embed/FmhnP44kmHU?si=xQjyMTj0IF9s_7RO" title="YouTube video player" frameBorder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowFullScreen></iframe>
                        <h2>Zakładka Obserwacje</h2>
                        <iframe className={"yt-video"} width="560" height="315" src="https://www.youtube.com/embed/2tQt-Yvwxb8?si=q3sH2ptae2D82n3E" title="YouTube video player" frameBorder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowFullScreen></iframe>
                        <h2>Zakładka Analiza</h2>
                        <iframe className={"yt-video"} width="560" height="315" src="https://www.youtube.com/embed/SZjyrjEbUkM?si=VXyihKMAVzSRFHuA" title="YouTube video player" frameBorder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowFullScreen></iframe>
                    </article>
                </div>
            </div>
        </div>
    );
}

export default About;