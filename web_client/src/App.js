import './App.css';
import { BrowserRouter, Routes, Route} from 'react-router-dom';
import MainPage from './pages/MainPage';
import About from './pages/About';
import PredictionPage from './pages/PredictionPage';
import ObservationsPage from './pages/ObservationsPage';
import AnalysisPage from './pages/AnalysisPage';
import Footer from "./components/Footer";
import { LocalizationProvider } from "@mui/x-date-pickers";
import {AdapterDayjs} from "@mui/x-date-pickers/AdapterDayjs";
import 'dayjs/locale/pl'

function App() {
  return (
    <div className="App">
        <LocalizationProvider dateAdapter={AdapterDayjs} adapterLocale='pl'>
            <BrowserRouter>
                <Routes>
                    <Route index element={<MainPage />} />
                    <Route path="/*" element={<MainPage />} />
                    <Route path="/o-projekcie" element={<About />} />
                    <Route path="/predykcja" element={<PredictionPage />} />
                    <Route path="/obserwacje" element={<ObservationsPage />} />
                    <Route path="/analiza" element={<AnalysisPage />} />
                    <Route path="/*" element={<MainPage />} />
                </Routes>
            </BrowserRouter>
        </LocalizationProvider>
        <Footer />
    </div>
  );
}

export default App;
