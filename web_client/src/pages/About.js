import Footer from "../components/Footer";
import TopNav from "../components/TopNav";
import aboutImg from '../assets/about_img_1.jpg'
import {useLocation} from "react-router-dom";

function About() {
    return (
        <div>
            <TopNav activePage={useLocation().pathname}/>
            <div className="main-container">
                <div className="article-container">
                    <article>
                        <img src={aboutImg} alt="kingfisher"/>
                        <h1>O projekcie</h1>
                        <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer id tellus quis elit rhoncus consectetur. Quisque pretium libero sed est maximus facilisis. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Maecenas fermentum, diam sed tristique tincidunt, elit diam bibendum dui, id commodo ipsum libero eget urna. Sed egestas magna non justo feugiat, sit amet suscipit risus sagittis. Fusce scelerisque sem nec neque sollicitudin auctor vel ut urna. Cras efficitur eros elit, ac consectetur justo condimentum condimentum. Curabitur sodales dapibus molestie.</p>
                        <p>Nullam vehicula purus eu ipsum interdum, a mollis urna semper. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Fusce quis ex et est consectetur faucibus. Ut condimentum felis nunc, vitae ultrices lorem pretium et. Nunc vulputate nunc ut erat pulvinar fringilla. Nam in diam porta, condimentum mi eget, sodales ipsum. Aliquam vel euismod lacus, ac vestibulum ante. Quisque nec urna id turpis molestie pulvinar vitae et magna. Mauris sit amet dui vel lorem porttitor dictum.</p>
                        <p>Sed luctus urna odio, at interdum ante dignissim eu. Quisque libero tortor, aliquam non dolor ac, volutpat scelerisque sem. Maecenas urna nibh, tincidunt id vulputate in, gravida et massa. Nullam risus tortor, venenatis eget pulvinar at, vestibulum a arcu. Sed posuere augue a ex elementum imperdiet. Duis feugiat condimentum leo, at laoreet turpis auctor id. Donec vitae semper augue. Maecenas vitae commodo tortor.</p>
                        <p>Fusce faucibus urna sit amet metus accumsan pharetra. Morbi dignissim nibh vel aliquam dapibus. Vivamus nec felis sit amet dui sollicitudin suscipit eu eu diam. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Cras eget risus luctus, euismod nulla ut, aliquet risus. Morbi dapibus eu purus id dictum. Pellentesque id sapien sed urna bibendum lobortis. Nullam semper pharetra magna at egestas. In sollicitudin purus urna, nec ultricies mi vehicula sit amet.</p>
                        <p>Maecenas et mollis erat. Pellentesque ut pulvinar elit. Morbi ut lacus arcu. Morbi sed eleifend mi. Maecenas facilisis nisl et fermentum porttitor. Ut sagittis ullamcorper scelerisque. Vestibulum varius tellus at quam cursus facilisis.</p>
                    </article>
                </div>
            </div>
        </div>
    );
}

export default About;