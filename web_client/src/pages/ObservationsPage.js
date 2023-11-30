import Footer from "../components/Footer";
import TopNav from "../components/TopNav";
import {Chart} from "react-google-charts";
import {useState, useEffect, useReducer} from "react";
import source from "../backendConfig";
import {json, useLocation} from "react-router-dom";

let dataPlaceholder1 = {
    "2013-07": {
        "dolnośląskie": 15.39,
        "kujawsko-pomorskie": 1.93,
        "lubelskie": 4.91,
        "województwo lubuskie": 5.33,
        "województwo mazowieckie": 2.38,
        "województwo małopolskie": 10.08,
        "województwo opolskie": 12.3,
        "województwo podkarpackie": 21.15,
        "województwo podlaskie": 4.6,
        "województwo pomorskie": 4.18,
        "województwo warmińsko-mazurskie": 0.87,
        "województwo wielkopolskie": 10.0,
        "województwo zachodniopomorskie": 6.91,
        "województwo łódzkie": 29.71,
        "województwo śląskie": 11.98,
        "województwo świętokrzyskie": 2.06
    },
    "2013-08": {
        "DOLNOSLASKIE": 2.6666666666666665,
        "KUJAWSKO_POMORSKIE": 3.0,
        "LODZKIE": 0.0,
        "LUBELSKIE": 0.0,
        "LUBUSKIE": 11.333333333333334,
        "MALOPOLSKIE": 0.0,
        "MAZOWIECKIE": 0.0,
        "OPOLSKIE": 0.0,
        "PODKARPACKIE": 0.0,
        "PODLASKIE": 1.0,
        "POMORSKIE": 1.0,
        "SLASKIE": 2.0,
        "SWIETOKRZYSKIE": 0.0,
        "WARMINSKO_MAZURSKIE": 0.0,
        "WIELKOPOLSKIE": 5.0,
        "ZACHODNIOPOMORSKIE": 14.5
    },
    "2013-09": {
        "DOLNOSLASKIE": 0.0,
        "KUJAWSKO-POMORSKIE": 0.0,
        "LODZKIE": 0.0,
        "LUBELSKIE": 1.0,
        "LUBUSKIE": 5.0,
        "MALOPOLSKIE": 2.0,
        "MAZOWIECKIE": 2.0,
        "OPOLSKIE": 0.0,
        "PODKARPACKIE": 0.0,
        "PODLASKIE": 1.0,
        "POMORSKIE": 0.0,
        "SLASKIE": 5.0,
        "SWIETOKRZYSKIE": 0.0,
        "WARMINSKO-MAZURSKIE": 0.0,
        "WIELKOPOLSKIE": 1.0,
        "ZACHODNIOPOMORSKIE": 8.666666666666666
    }
};

const regionsOfPoland = ["dolnośląskie",
    "kujawsko-pomorskie",
    "łódzkie",
    "lubelskie",
    "lubuskie",
    "małopolskie",
    "mazowieckie",
    "opolskie",
    "podkarpackie",
    "podlaskie",
    "pomorskie",
    "śląskie",
    "świętokrzyskie",
    "warmińsko-mazurskie",
    "wielkopolskie",
    "zachodniopomorskie"]

let data = [
    [["Region", "Bird encounters"],
        ["USA", 100]]

];

let months = ["2023.09", "2023.10"];

let data2 = [
    ["Latitude", "Longitude", "Encounter number"],
    [54.48208741195183, 18.217575002051657, 10],
    [54.482012483, 18.217575002051657, 20],
    [54.4124195183, 18.217575002051657, 30],
    [54.48208741195183, 18.37575002051657, 220],
    [54.1238741195183, 18.2234002051657, 1],
    [54.4821241195183, 18.212302051657, 10],
    [54.482012495183, 18.217521457, 10],
    [54.482124111195183, 18.212475002051657, 10],
    [54.48208741195183, 18.2171242051657, 10],
    [53.36893734031183, 18.22842592671696, 3]
]
let options = {
    region: "PL",
    displayMode: "regions",
    resolution: "provinces",
    colorAxis: {minValue: 0, maxValue: 1000, colors: ["#ffe3e3", "#ff0000"]}
};

let options2 = {
    region: "PL",
    displayMode: "markers",
    resolution: "provinces",
    sizeAxis: {minValue: 1, maxValue: 100},
    colorAxis: {colors: ["#ffe3e3", "#ff0000"]},
};

function ObservationsPage() {

    function handleFilterChange(event) {
        if (event.target.value === "") {
            setFilteredBirdSpecies(birdSpecies);
        } else {
            setFilteredBirdSpecies(birdSpecies.filter((species) => species.text.toLowerCase().includes(event.target.value.toLowerCase())));
        }
    }

    function handleSpeciesChange(event, speciesCommonName) {
        setChosenBirdCommonName(speciesCommonName);
        setChosenBirdScientificName(event.target.value);
    }

    function handleDateFromChange(event) {
        setChosenDateFrom(event.target.value);
        console.log(event.target.value);
    }

    function handleDateToChange(event) {
        setChosenDateTo(event.target.value);
        console.log(event.target.value);
    }

    async function handleSubmit(event) {
        event.preventDefault();
        // Form validation
        setChosenBirdScientificNameError("");
        setChosenDateFromError("");
        setChosenDateToError("");
        setAnyError("");

        let valid = true;

        if (chosenBirdScientificName === "") {
            setChosenBirdScientificNameError("Brak wybranego gatunku");
            valid = false;
        }
        if (chosenDateFrom === "") {
            setChosenDateFromError("Brak wybranej daty");
            valid = false;
        }
        if (chosenDateTo === "") {
            setChosenDateToError("Brak wybranej daty");
            valid = false;
        }
        if (chosenDateTo < chosenDateFrom) {
            setChosenDateFromError("Niepoprawne daty");
            setChosenDateToError("Niepoprawne daty");
            valid = false;
        }
        if (!valid) {
            console.log("error");
            setAnyError("Błąd formularza");
            return;
        }


        let url = `${source}birds/${chosenBirdScientificName}/observations?from=${chosenDateFrom}&to=${chosenDateTo}`;


        // TODO - CHANGE predictionData FROM  [[]] to [] and Refactor names on this page

        setIsLoading(true);
        await fetch(url)
            .then(response => response.json())
            .then(data => {
                console.log(data);
                const observationKeys = Object.keys(data.observations);
                let allObservations = [];
                let maxObservationsValue = 0;

                let observations = [["latitude", "longitude", "observation count", {
                    role: "tooltip",
                    type: "string",
                    p: {html: true}
                }]];
                observationKeys.forEach(key => {
                    let observationDate = new Date(data.observations[key]["observation date"]);

                    observations.push([data.observations[key]["latitude"], data.observations[key]["longitude"], data.observations[key]["observation count"],
                        `<p><span class="weight-700">Liczba osobników:</span> ${data.observations[key]["observation count"]}</p>
                        <p><span class="weight-700">Data obserwacji:</span> ${observationDate.toDateString()}</p>`]);
                    if (data.observations[key]["observation count"] > maxObservationsValue) {
                        maxObservationsValue = data.observations[key]["observation count"];
                    }

                    allObservations.push(observations);
                });

                setPredictionSpecies(chosenBirdCommonName);
                if(data.observations.length === 0) {
                    return;
                }
                setPredictionData(allObservations);
                setPredictionMonths(0);
                predictionDispatch({type: 'month_setup', maxMonthNumber: 0});
                setMapOptions({
                    region: "PL",
                    displayMode: "markers",
                    resolution: "provinces",
                    sizeAxis: {minValue: 1, maxValue: maxObservationsValue},
                    colorAxis: {minValue: 0, maxValue: maxObservationsValue, colors: ["#ffbbbb", "#ff0000"]},
                    tooltip: {isHtml: true, trigger: "visible"}
                });
            })
            .catch(error => console.error(error));
        setIsLoading(false);
    }

    function predictionReducer(state, action) {
        switch (action.type) {
            case 'month_increment': {
                if (state.currentMonth === state.maxMonth) {
                    return {
                        maxMonth: state.maxMonth,
                        currentMonth: 0
                    };
                }
                return {
                    maxMonth: state.maxMonth,
                    currentMonth: state.currentMonth + 1
                };
            }
            case 'month_decrement': {
                if (state.currentMonth === 0) {
                    return {
                        maxMonth: state.maxMonth,
                        currentMonth: state.maxMonth
                    };
                }
                return {
                    maxMonth: state.maxMonth,
                    currentMonth: state.currentMonth - 1
                };
            }
            case 'month_setup': {
                return {
                    maxMonth: action.maxMonthNumber,
                    currentMonth: 0
                };
            }
            default: {
                return {
                    maxMonth: state.maxMonth,
                    currentMonth: state.currentMonth
                };
            }
        }

    }

    const [region, setRegion] = useState("");
    const [areBirdsFetched, setAreBirdsFetched] = useState("f");
    const [predictionTypes, setPredictionTypes] = useState([]);
    const [birdSpecies, setBirdSpecies] = useState([]);
    const [filteredBirdSpecies, setFilteredBirdSpecies] = useState([]);
    // 
    // Form variables
    const [chosenBirdCommonName, setChosenBirdCommonName] = useState("");
    const [chosenBirdScientificName, setChosenBirdScientificName] = useState("");
    const [chosenModel, setChosenModel] = useState("");
    const [chosenDateFrom, setChosenDateFrom] = useState("");
    const [chosenDateTo, setChosenDateTo] = useState("");
    const [defaultOptions, setDefaultOptions] = useState(true);
    const [rangeValue1, setRangeValue1] = useState(24); // TODO - change later to get this value fetched after model is chosen
    // Form error information
    const [chosenBirdScientificNameError, setChosenBirdScientificNameError] = useState("");
    const [chosenModelError, setChosenModelError] = useState("");
    const [chosenDateFromError, setChosenDateFromError] = useState("");
    const [chosenDateToError, setChosenDateToError] = useState("");
    const [anyError, setAnyError] = useState("");

    // Prediction visualization
    const [predictionState, predictionDispatch] = useReducer(predictionReducer, {currentMonth: 0, maxMonth: 1});
    const [currentPredictionMonth, setCurrentPredictionMonth] = useState(months[0]);
    const [predictionData, setPredictionData] = useState(data);
    const [predictionErrorData, setPredictionErrorData] = useState(data);
    const [predictionMonths, setPredictionMonths] = useState([]);
    const [predictionSpecies, setPredictionSpecies] = useState("");
    const [isPredictionGenerated, setIsPredictionGenerated] = useState(false);
    const [isLoading, setIsLoading] = useState(false);
    const [isErrorGenerated, setIsErrorGenerated] = useState(true);
    const [isAnimationPlaying, setIsAnimationPlaying] = useState(false);
    const [isShowingErrors, setIsShowingErrors] = useState(false);
    const [mapOptions, setMapOptions] = useState({
        region: "PL",
        displayMode: "regions",
        resolution: "provinces",
        colorAxis: {minValue: 0, maxValue: 0, colors: ["#ffffff", "#ff0000"]}
    });

    useEffect(() => {

        let predictionMonthNumber = 0;

        const interval = setInterval(() => {
            if (isAnimationPlaying) {
                predictionDispatch({type: 'month_increment'});
            }
        }, 2000);

        return () => clearInterval(interval);
    }, [isAnimationPlaying, isPredictionGenerated, predictionState.currentMonth]);

    // Fetching available bird species 
    useEffect(() => {
        fetch(source + "birds")
            .then(response => response.json())
            .then(data => {
                const speciesPromises = data.species.map(species => {
                    return fetch(source + "birds/" + species)
                        .then(response => response.json())
                        .then(birdData => {
                            let bird = {name: species, text: birdData.common_name};
                            return bird;
                        })
                        .catch(error => console.error(error));
                });
                return Promise.all(speciesPromises);
            })
            .then(fetchedSpecies => {
                setBirdSpecies(fetchedSpecies);
            })
            .catch(error => console.error(error));
    }, []);

    useEffect(() => {
        setFilteredBirdSpecies(birdSpecies);
    }, [birdSpecies]);

    return (
        <div>
            <TopNav activePage={useLocation().pathname}/>
            {isLoading && <div className="modal-info">Ładowanie...</div>}
            <div className="columns-container">
                <div className="column-l">
                    <div className="column-content small-screen-text-center">
                        <div>
                            <span className="map-header">Zarejestrowane obserwacje</span>
                            <a href="#prediction-menu">
                                <button className="anchor-button">Przejdź do opcji</button>
                            </a>
                            <span className="map-prediction-info">Wybrany gatunek: <span
                                className="map-info-highlight">{predictionSpecies}</span></span>
                        </div>
                        <div className="map-container observations-map-container">
                            <Chart className="map" chartType="GeoChart"
                                   data={predictionData[predictionState.currentMonth]} options={mapOptions}/>
                        </div>
                        <div className="map-info-container">
                        </div>
                    </div>
                </div>
                <div className="column-r">
                    <div className="column-content prediction-column">
                        <a id="prediction-menu"></a>
                        <span className={anyError ? "form-error-label map-header" : "map-header"}>Opcje:</span>
                        <div className="prediction-menu-container">
                            <form onSubmit={handleSubmit}>
                                <ul className="prediction-menu">
                                    <li key='form-part-1'>
                                        <input type="submit" value="Sprawdź obserwacje"></input>
                                    </li>
                                    <li key='form-part-2'>
                                        <label
                                            className={chosenDateFromError ? "form-error-label" : "form-default-label"}
                                            htmlFor="prediction-date-from">Wybierz datę początkową okresu
                                            obserwacji</label>
                                        <input type="date" id="prediction-date-from" name="prediction-date-from"
                                               onChange={e => handleDateFromChange(e)}/>
                                        {chosenDateFromError &&
                                            <span className="form-error">{chosenDateFromError}</span>}
                                        <label className={chosenDateToError ? "form-error-label" : "form-default-label"}
                                               htmlFor="prediction-date-to">Wybierz datę końcową okresu
                                            obserwacji</label>
                                        <input type="date" id="prediction-date-to" name="prediction-date-to"
                                               onChange={e => handleDateToChange(e)}/>
                                        {chosenDateToError && <span className="form-error">{chosenDateToError}</span>}
                                    </li>
                                    <li key='form-part-3'>
                                        <span
                                            className={chosenBirdScientificNameError ? "form-error-label" : "form-default-label"}>Wybierz gatunek ptaka:</span>
                                        <input type="text" id="species-filter" onChange={handleFilterChange}
                                               placeholder="orzeł bielik... "/>
                                        <div className="bird-species-choice-container">
                                            {birdSpecies.map(species => (
                                                <div key={species.name}
                                                     className={filteredBirdSpecies.includes(species) ? 'bird-species-container' : 'bird-species-container unfiltered'}>
                                                    <input type="radio" id={species.name} value={species.name}
                                                           name="bird-species"
                                                           onChange={e => handleSpeciesChange(e, species.text)}/>
                                                    <label className="radio-label"
                                                           htmlFor={species.name}>{species.text}</label>
                                                </div>
                                            ))}
                                        </div>
                                        {chosenBirdScientificNameError &&
                                            <span className="form-error">{chosenBirdScientificNameError}</span>}
                                    </li>
                                </ul>
                            </form>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default ObservationsPage;