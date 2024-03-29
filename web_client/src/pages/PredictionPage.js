import TopNav from "../components/TopNav";
import {Chart} from "react-google-charts";
import {useState, useEffect, useReducer} from "react";
import source from "../backendConfig";
import {useLocation} from "react-router-dom";
import {DatePicker} from "@mui/x-date-pickers";
import dayjs from 'dayjs';
import {Slider} from "@mui/material";

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
    "zachodniopomorskie"];

let data = [
    [["Region", "Bird encounters"],
        ["USA", 100]]

];

function PredictionPage() {

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

    function handleRangeChange(event) {
        setSliderChange(-sliderChange);
        let optionRanges = chosenCustomOptions;
        optionRanges[event.target.name] = event.target.value;
        setChosenCustomOptions(optionRanges);
    }

    function handleModelChange(event) {
        setChosenModel(event.target.value);
    }

    function handleOptionChange(option) {
        setDefaultOptions(option);
    }

    function handleDateFromChange(value) {
        setChosenDateFrom(dayjs(value).format('YYYY-MM'));
    }

    function handleDateToChange(value) {
        setChosenDateTo(dayjs(value).format('YYYY-MM'));
    }

    async function handleSubmit(event) {
        event.preventDefault();
        // Form validation
        setChosenBirdScientificNameError("");
        setChosenModelError("");
        setChosenDateFromError("");
        setChosenDateToError("");
        setAnyError("");

        let valid = true;

        if (chosenBirdScientificName === "") {
            setChosenBirdScientificNameError("Brak wybranego gatunku");
            valid = false;
        }
        if (chosenModel === "") {
            setChosenModelError("Brak wybranego modelu");
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

        let customOptionsKeys = Object.keys(chosenCustomOptions);
        let optionParms ="";
        customOptionsKeys.forEach(customOptionKey => {
            optionParms += `&${customOptionKey}=${chosenCustomOptions[customOptionKey]}`;
        })
        let url;
        if (!defaultOptions) {
            url = `${source}birds/${chosenBirdScientificName}/models/${chosenModel}/predict?from=${chosenDateFrom}&to=${chosenDateTo}${optionParms}&edge=2021-12`;
        } else {
            url = `${source}birds/${chosenBirdScientificName}/models/${chosenModel}/predict?from=${chosenDateFrom}&to=${chosenDateTo}&edge=2021-12`;
        }

        setIsLoading(true);

        await fetch(url)
            .then(response => response.json())
            .then(data => {
                let dataPlaceholder = data.predictions; // change dataPlaceholder to another name
                let wholePrediction = [];
                let maxPredictionValue = 0;
                const months = Object.keys(dataPlaceholder);
                months.forEach(month => {
                    const places = Object.keys(dataPlaceholder[month]);
                    let monthlyPrediction = [["Region", "Średnia liczba zaobserwowanych osobników"]];
                    places.forEach(place => {
                        monthlyPrediction.push([place, dataPlaceholder[month][place]]);
                        if (dataPlaceholder[month][place] > maxPredictionValue) {
                            maxPredictionValue = dataPlaceholder[month][place];
                        }
                    });
                    wholePrediction.push(monthlyPrediction);
                });

                // Prediction error
                let errorData = data.custom_errors;
                let predictionErrors = [["Region", "Błąd predykcji"]];
                const regions = Object.keys(errorData);
                let maxPredictionError = 0;
                regions.forEach(region => {
                    predictionErrors.push([region, data.custom_errors[region]]);
                    if (maxPredictionError < data.custom_errors[region]) {
                        maxPredictionError = data.custom_errors[region];
                    }
                })
                if (regions.length > 0) {
                    setIsErrorGenerated(true);
                } else {
                    setIsErrorGenerated(false);
                }
                setPredictionErrorData(predictionErrors);
                setMapErrorOptions({
                    region: "PL",
                    displayMode: "regions",
                    resolution: "provinces",
                    colorAxis: {minValue: 0, maxValue: 1, colors: ["#ffffff", "#0000ff"]}
                });

                setPredictionData(wholePrediction);
                setPredictionMonths(months);
                predictionDispatch({type: 'month_setup', maxMonthNumber: months.length - 1});
                setMapOptions({
                    region: "PL",
                    displayMode: "regions",
                    resolution: "provinces",
                    colorAxis: {minValue: 0, maxValue: maxPredictionValue, colors: ["#ffffff", "#ff0000"]}
                });
                setIsPredictionGenerated(true);
                setIsAnimationPlaying(true);
                setPredictionSpecies(chosenBirdCommonName);
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
    const [sliderChange, setSliderChange] = useState(1);

    const [predictionTypes, setPredictionTypes] = useState([]);
    const [birdSpecies, setBirdSpecies] = useState([]);
    const [filteredBirdSpecies, setFilteredBirdSpecies] = useState([]);
    const [predictionOptions, setPredictionOptions] = useState([]);
    // 
    // Form variables
    const [chosenBirdCommonName, setChosenBirdCommonName] = useState("");
    const [chosenBirdScientificName, setChosenBirdScientificName] = useState("");
    const [chosenModel, setChosenModel] = useState("");
    const [chosenDateFrom, setChosenDateFrom] = useState("");
    const [chosenDateTo, setChosenDateTo] = useState("");
    const [defaultOptions, setDefaultOptions] = useState(true);
    const [chosenCustomOptions, setChosenCustomOptions] = useState({});
    // Form error information
    const [chosenBirdScientificNameError, setChosenBirdScientificNameError] = useState("");
    const [chosenModelError, setChosenModelError] = useState("");
    const [chosenDateFromError, setChosenDateFromError] = useState("");
    const [chosenDateToError, setChosenDateToError] = useState("");
    const [anyError, setAnyError] = useState("");

    // Prediction visualization
    const [predictionState, predictionDispatch] = useReducer(predictionReducer, {currentMonth: 0, maxMonth: 1});
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
    const [mapErrorOptions, setMapErrorOptions] = useState({
        region: "PL",
        displayMode: "regions",
        resolution: "provinces",
        colorAxis: {minValue: 0, maxValue: 0, colors: ["#ffffff", "#ff0000"]}
    });
    useEffect(() => {

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
                            let bird = {name: species, text: birdData.common_name, wiki: birdData.wiki, ebird: birdData.ebird};
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

    // Fetching available prediction models for certain species
    useEffect(() => {
        if (chosenBirdScientificName) {
            fetch(source + "birds/" + chosenBirdScientificName + "/models")
                .then(response => response.json())
                .then(modelsData => modelsData.supported_models.map(model => {
                    return ({name: model.value, text: model.display})
                }))
                .then(models => {
                    setPredictionTypes(models);
                    // CHECK IF ITS WORKING WHEN MORE MODELS ARE BE ADDED
                    if (chosenModel !== "") {
                        let isAvailable = false;
                        models.forEach(model => {
                            if (model.name === chosenModel) {
                                isAvailable = true;
                            }
                        });
                        if (!isAvailable) {
                            setChosenModel("");
                        }
                    }
                })
                .catch(error => {
                    console.error(error);
                    setPredictionTypes([]);
                });
        }
    }, [chosenBirdScientificName]);

    // Fetching available options for certain prediction model
    useEffect(() => {
        setPredictionOptions([]);
        setChosenCustomOptions({});

        if (chosenModel) {
            fetch(source + "birds/" + chosenBirdScientificName + "/models/" + chosenModel)
                .then(response => response.json())
                .then(options => {
                    let availableOptions = [];
                    let chosenOptions = {};
                    const optionNames = Object.keys(options);
                    optionNames.forEach(optionName => {
                        availableOptions.push({option_type: optionName, option_name: options[optionName]["pl_name"],
                            option_default: options[optionName]["default"], option_max: options[optionName]["max"], option_min: options[optionName]["min"]});
                        chosenOptions[optionName] = options[optionName]["default"];
                    });
                    setPredictionOptions(availableOptions);
                    setChosenCustomOptions(chosenOptions);
                })
                .catch(error => {
                    console.error(error);
                    setPredictionTypes([]);
                });
        }
    }, [chosenModel, chosenBirdScientificName]);

    return (
        <div>
            <TopNav activePage={useLocation().pathname}/>
            {isLoading && <div className="modal-info">Ładowanie...</div>}
            <div className="columns-container">
                <div className="column-l">
                    <div className="column-content small-screen-text-center">
                        <div>
                            <span className="map-header">Predykcja występowania ptaków</span>
                            <a href="#prediction-menu">
                                <button className="anchor-button">Przejdź do predykcji</button>
                            </a>
                            <span className="map-prediction-info">Wybrany gatunek: <span
                                className="map-info-highlight">{predictionSpecies}</span></span>
                            <span className="map-prediction-info">Aktualny miesiąc predykcji: <span
                                className="map-info-highlight">{predictionMonths[predictionState.currentMonth]}</span></span>
                            <div className="animation-menu-container">
                                <ul className="animation-menu">
                                    <li>
                                        <button disabled={!isPredictionGenerated || isShowingErrors}
                                                className="animation-button" onClick={() => {
                                            predictionDispatch({type: 'month_decrement'})
                                        }}>{'<'}</button>
                                    </li>
                                    <li>
                                        <button disabled={!isPredictionGenerated || isShowingErrors}
                                                className="animation-button"
                                                onClick={() => setIsAnimationPlaying(!isAnimationPlaying)}>{isAnimationPlaying ? "STOP" : "PLAY"}</button>
                                    </li>
                                    <li>
                                        <button disabled={!isPredictionGenerated || isShowingErrors}
                                                className="animation-button" onClick={() => {
                                            predictionDispatch({type: 'month_increment'})
                                        }}>{'>'}</button>
                                    </li>
                                </ul>
                            </div>
                        </div>
                        <div className="map-container">
                            <Chart className="map" chartType="GeoChart"
                                   data={!isShowingErrors ? predictionData[predictionState.currentMonth] : predictionErrorData}
                                   options={!isShowingErrors ? mapOptions : mapErrorOptions}
                                   chartEvents={[
                                       {
                                           eventName: "select",
                                           callback: ({chartWrapper}) => {
                                               const chart = chartWrapper.getChart();
                                               const selection = chart.getSelection();
                                               //if (selection.length === 0) return;
                                               //const chosenRegion = regionsOfPoland[selection[0].row];
                                           },
                                       },
                                   ]}/>
                        </div>
                        <div className="map-info-container">
                            <button disabled={!isPredictionGenerated || !isErrorGenerated} className="error-button"
                                    onClick={() => {
                                        setIsAnimationPlaying(isShowingErrors);
                                        setIsShowingErrors(!isShowingErrors)
                                    }}>{!isShowingErrors ? "Pokaż błędy predykcji" : "Pokaż wyniki predykcji"}</button>
                            {!isErrorGenerated && <div className="no-prediction-error">Brak dostępnych danych</div>}
                        </div>
                    </div>
                </div>
                <div className="column-r">
                    <div className="column-content prediction-column">
                        <span id="prediction-menu" className={anyError ? "form-error-label map-header" : "map-header"}>Opcje:</span>
                        <div className="prediction-menu-container">
                            <form onSubmit={handleSubmit}>
                                <ul className="prediction-menu">
                                    <li key='form-part-1'>
                                        <input type="submit" value="Wykonaj predykcje"></input>
                                    </li>
                                    <li key='form-part-2'>
                                        <label
                                            className={chosenDateFromError ? "form-error-label" : "form-default-label"}
                                            htmlFor="prediction-date-from">Wybierz datę początkową predykcji</label>
                                        <div className="pg-custom-mui-input"><DatePicker views={['month', 'year']} onChange={(v) => handleDateFromChange(v)}
                                                    slotProps={{
                                                        field:{
                                                        id:'prediction-date-from'
                                                        }
                                                    }} /></div>
                                        {chosenDateFromError &&
                                            <span className="form-error">{chosenDateFromError}</span>}
                                        <label className={chosenDateToError ? "form-error-label" : "form-default-label"}
                                               htmlFor="prediction-date-to">Wybierz datę końcową predykcji</label>
                                        <div className="pg-custom-mui-input">
                                            <DatePicker views={['month', 'year']}
                                                        onChange={(v) => handleDateToChange(v)}
                                                        slotProps={{
                                                            field:{
                                                                id:'prediction-date-to'
                                                            }
                                                        }
                                            } />
                                        </div>
                                        {chosenDateToError && <span className="form-error">{chosenDateToError}</span>}
                                    </li>
                                    <li key='form-part-3'>
                                        <span className="form-default-label">Wybierz opcje modelu:</span>
                                        { chosenModel === "" ?
                                            <div className='prediction-types-placeholder'>Zaznacz model predykcji, aby
                                                zobaczyć dostępne opcje</div> :
                                            <div>
                                            <div className='prediction-option-container'> {/* TODO modelsOptions.map() */}
                                                <input type="radio" id="prediction-default" value="prediction-default"
                                                       name="prediction-option" defaultChecked
                                                       onChange={e => handleOptionChange(true)}/>
                                                <label className="radio-label" htmlFor="prediction-default">standardowe
                                                    (zalecane)</label>
                                            </div>
                                            <div className='prediction-option-container'>
                                                <input type="radio" id="prediction-non-default"
                                                       value="prediction-non-default" name="prediction-option"
                                                       onChange={e => handleOptionChange(false)}/>
                                                <label className="radio-label"
                                                       htmlFor="prediction-non-default">niestandardowe</label>
                                            </div>
                                            <div>
                                            {(!defaultOptions && predictionOptions.length > 0)
                                                && predictionOptions.map(predictionOption =>
                                                <div>
                                                    <div className='prediction-option-container'>
                                                        <span className="form-default-label">{predictionOption["option_name"]}: </span>
                                                        <span className="range-value">{chosenCustomOptions[predictionOption["option_type"]]}</span>
                                                        <div className="pg-custom-mui-input">
                                                            <Slider name={predictionOption["option_type"]} min={predictionOption["option_min"]} max={predictionOption["option_max"]} defaultValue={predictionOption["option_default"]}
                                                                    onChange={e => handleRangeChange(e)}
                                                                    slotProps={{
                                                                        input:{
                                                                            id:predictionOption["option_type"]
                                                                        }
                                                                    }}
                                                            />
                                                        </div>
                                                    </div>
                                                </div>
                                                )
                                            }
                                            </div>
                                        </div>
                                        }
                                    </li>
                                    <li key='form-part-4'>
                                        <span className={chosenModelError ? "form-error-label" : "form-default-label"}>Wybierz rodzaj predykcji:</span>
                                        {predictionTypes.length === 0 ?
                                            <div className='prediction-types-placeholder'>Zaznacz gatunek ptaka, aby
                                                zobaczyć dostępne modele</div> : predictionTypes.map(predictionType =>
                                                <div key={predictionType.name} className='prediction-type-container'>
                                                    <input type="radio" id={predictionType.name}
                                                           value={predictionType.name} name="prediction-type"
                                                           onChange={e => handleModelChange(e)}/>
                                                    <label className="radio-label"
                                                           htmlFor={predictionType.name}>{predictionType.text}</label>
                                                </div>
                                            )}
                                        {chosenModelError && <span className="form-error">{chosenModelError}</span>}
                                    </li>
                                    <li key='form-part-5'>
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
                                                    {(species.wiki || species.ebird) && <div className={"bird-info"}>
                                                        <span className={"bird-info-icon"}>INFO</span>
                                                        <div className={"bird-info-links"}>
                                                            <div className={"bird-info-link"}>
                                                                {species.wiki && <a href={species.wiki}>Wikipedia</a>}
                                                            </div>
                                                            <div className={"bird-info-link"}>
                                                                {species.ebird && <a href={species.ebird}>Ebird</a>}
                                                            </div>
                                                        </div>
                                                    </div>}
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

export default PredictionPage;