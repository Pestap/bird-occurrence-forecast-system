import Footer from "../components/Footer";
import TopNav from "../components/TopNav";
import XbuttonSlim from "../components/svg/XbuttonSlim";
import {Chart} from "react-google-charts";
import {useState, useEffect, useReducer} from "react";
import source from "../backendConfig";
import {json, useLocation} from "react-router-dom";
import VisibilityIcon from "../components/svg/VisiblityIcon";
import InvisibilityIcon from "../components/svg/InvisibiltyIcon";

export const dataTest = [
    ["Year", "Sales", "Expenses"],
    ["2004", 1000, null],
    ["2005", 1170, null],
    ["2006", 660, 660],
    ["2007", 1030, 999],
];
export const optionsTest = {
    title: "Company Performance",
    curveType: "function",
    legend: { position: "bottom" },
};

const regionsPlaceHolder = ["dolnośląskie",
    "kujawsko-pomorskie",
    "lubelskie",
    "lubuskie",
    "mazowieckie",
    "małopolskie",
    "opolskie",
    "podkarpackie",
    "podlaskie",
    "pomorskie",
    "warmińsko-mazurskie",
    "wielkopolskie",
    "zachodniopomorskie",
    "łódzkie",
    "śląskie",
    "świętokrzyskie"];

let data = [
    [["Region", "Bird encounters"],
        ["USA", 100]]

];

let months = ["2023.09", "2023.10"];

let DEFAULT_PLOT_COLOR = "#FF0000"

function AnalysisPage() {

    function handleModelRemove(modelId) {
        setAnalysisModels(analysisModels.filter(analysisModel => analysisModel.id !== modelId));
    }

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
        // TODO - Set chosen model to "" or uncheck radio buttons, if it has different available models, like setChosenModel("");
    }

    function handleRangeChange(event, rangeNumber) {
        console.log(event.target.name);

        let optionRanges = chosenCustomOptions;
        optionRanges[event.target.name] = event.target.value;
        setChosenCustomOptions(optionRanges);

        // TODO REMOVE THESE 2 LINES
        if (rangeNumber === 1) {
            setRangeValue1(event.target.value);
        }
    }

    function handleModelChange(event) {
        setChosenModel(event.target.value);
        console.log(event.target.value);
    }

    function handleOptionChange(option) {
        setDefaultOptions(option);
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
        // TODO - Instead of checking single model - check if at least one is added
        // TODO - then map each model to fetch some data and store it in some array
        event.preventDefault();
        // Form validation
        setChosenBirdScientificNameError("");
        setChosenModelsError("");
        setChosenDateFromError("");
        setChosenDateToError("");
        setAnyError("");
        let valid = true;

        if (chosenBirdScientificName === "") {
            setChosenBirdScientificNameError("Brak wybranego gatunku");
            valid = false;
        }
        if (analysisModels.length === 0) {
            setChosenModelsError("Brak wybranego modelu");
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

        setIsLoading(true);
        
        let emptyArr = modelsPredictions;
        emptyArr.length = 0;
        setModelsPredictions(emptyArr);

        let allModelsPredictions = [];

        await Promise.all(analysisModels.map(analysisModel => {

            let customOptions = Object.assign({}, analysisModel);
            delete customOptions.type;
            delete customOptions.color;
            delete customOptions.id;
            delete customOptions.visibility;
            delete customOptions.defaultOptions;

            let customOptionsKeys = Object.keys(customOptions);
            let optionParms ="";
            customOptionsKeys.forEach(customOptionKey => {
                optionParms += `&${customOptionKey}=${customOptions[customOptionKey]}`;
            })
            let url = "";
            if (!analysisModel.defaultOptions) {
                url = `${source}birds/${chosenBirdScientificName}/models/${analysisModel.type}/predict?from=${chosenDateFrom}&to=${chosenDateTo}${optionParms}&edge=2022-01-01`;
            } else {
                url = `${source}birds/${chosenBirdScientificName}/models/${analysisModel.type}/predict?from=${chosenDateFrom}&to=${chosenDateTo}&edge=2022-01-01`;
            }

            return fetch(url)
                .then(response => response.json())
                .then(data => {
                    let dataPlaceholder = data.predictions; // change dataPlaceholder to another name
                    let wholePrediction = [];
                    let maxPredictionValue = 0;
                    console.log(data.mae_errors);
                    const months = Object.keys(dataPlaceholder);
                    setChartMonths(months);
                    setChartTests(data.tests);
                    months.forEach(month => {
                        const places = Object.keys(dataPlaceholder[month]);
                        let monthlyPrediction = [["Region", "Bird encounters"]];
                        places.forEach(place => {
                            monthlyPrediction.push([place, dataPlaceholder[month][place]]);
                            if (dataPlaceholder[month][place] > maxPredictionValue) {
                                maxPredictionValue = dataPlaceholder[month][place];
                            }
                        });
                        wholePrediction.push(monthlyPrediction);
                    });
                    let generatedModelPredictionWithInfo = {"prediction": wholePrediction, "type": analysisModel.type, "id": analysisModel.id};
                    return generatedModelPredictionWithInfo;
                })
                .catch(error => console.error(error));
        }))
            .then(predictions => {
                setAppliedDateFrom(chosenDateFrom);
                return predictions;
            })
            .then(predictions => predictions.map(prediction => {
                console.log(prediction);
                allModelsPredictions = [...allModelsPredictions, prediction];
                //let currentModelsPredictions = [...modelsPredictions];
                //currentModelsPredictions.push(prediction);
                //setModelsPredictions(currentModelsPredictions);
            }))
            .then(p => {
                setModelsPredictions(allModelsPredictions)
            })
            .catch(error => console.error(error));
        setIsLoading(false);
        console.log(modelsPredictions);
    }

    function handleModelSubmit(event) {
        event.preventDefault();
        // Form validation
        setChosenModelError("");
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

        if (!valid) {
            console.log("error");
            setAnyError("Błąd formularza");
            return;
        }

        let modelsInfo = {};
        modelsInfo["type"] = chosenModel;
        modelsInfo["color"] = chosenColor;
        modelsInfo["id"] = currentModelId;
        modelsInfo["visibility"] = true;
        modelsInfo["defaultOptions"] = defaultOptions;
        Object.assign(modelsInfo, chosenCustomOptions);
        setAnalysisModels([
            ...analysisModels,
            modelsInfo // and one new item at the end
        ]);
        setChosenColor(DEFAULT_PLOT_COLOR);
        setCurrentModelId(currentModelId + 1);
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
    const [predictionOptions, setPredictionOptions] = useState([]);
    // Analysis variables
    const [analysisModels, setAnalysisModels] = useState([]);
    const [currentModelId, setCurrentModelId] = useState(0);
    const [changedVisibility, setChangedVisibility] = useState(false);
    const [availableRegions, setAvailableRegions] = useState([...regionsPlaceHolder]);
    const [chosenRegion, setChosenRegion] = useState(regionsPlaceHolder[0]);
    const [chartOptions, setChartOptions] = useState({
        title: "Średnia liczba osobników podczas obserwacji",
        legend: { position: "bottom" },
    });
    const [chartMonths, setChartMonths] = useState([]);
    const [chartTests, setChartTests] = useState([]);
    const [chartFinalData, setChartFinalData] = useState([]);
    const [chartFinalDataFiltered, setChartFinalDataFiltered] = useState([]);
    const [appliedDateFrom, setAppliedDateFrom] = useState("");
    // Form variables
    const [chosenBirdCommonName, setChosenBirdCommonName] = useState("");
    const [chosenBirdScientificName, setChosenBirdScientificName] = useState("");
    const [chosenModel, setChosenModel] = useState("");
    const [chosenDateFrom, setChosenDateFrom] = useState("");
    const [chosenDateTo, setChosenDateTo] = useState("");
    const [chosenColor, setChosenColor] = useState(DEFAULT_PLOT_COLOR);
    const [defaultOptions, setDefaultOptions] = useState(true);
    const [rangeValue1, setRangeValue1] = useState(24); // TODO - change later to get this value fetched after model is chosen
    const [chosenCustomOptions, setChosenCustomOptions] = useState({});
    // Form error information
    const [chosenBirdScientificNameError, setChosenBirdScientificNameError] = useState("");
    const [chosenModelError, setChosenModelError] = useState("");
    const [chosenDateFromError, setChosenDateFromError] = useState("");
    const [chosenDateToError, setChosenDateToError] = useState("");
    const [chosenModelsError, setChosenModelsError] = useState("");
    const [anyError, setAnyError] = useState("");

    // Prediction visualization
    const [modelsPredictions, setModelsPredictions] = useState([]);
    const [predictionState, predictionDispatch] = useReducer(predictionReducer, {currentMonth: 0, maxMonth: 1});
    const [currentPredictionMonth, setCurrentPredictionMonth] = useState(months[0]);
    const [predictionData, setPredictionData] = useState(data);
    const [predictionErrorData, setPredictionErrorData] = useState(data);
    const [predictionMonths, setPredictionMonths] = useState([]);
    const [predictionSpecies, setPredictionSpecies] = useState("");
    const [isPredictionGenerated, setIsPredictionGenerated] = useState(false);
    const [isErrorGenerated, setIsErrorGenerated] = useState(true);
    const [isAnimationPlaying, setIsAnimationPlaying] = useState(false);
    const [isShowingErrors, setIsShowingErrors] = useState(false);
    const [isLoading, setIsLoading] = useState(false);
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

    // Fetching available prediction models for certain species
    useEffect(() => {
        if (chosenBirdScientificName) {
            fetch(source + "birds/" + chosenBirdScientificName + "/models")
                .then(response => response.json())
                .then(modelsData => modelsData.supported_models.map(model => {
                    return ({name: model, text: model})
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
                        availableOptions.push({option_type: optionName, option_name: optionName,
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

    // Changing chart options
    useEffect(() => {
        if (analysisModels.length > 0) {

            let colors = {};
            let colorsArr = [];
            let i= 0;
            for(i=0;i<analysisModels.length;i++) {
                if(analysisModels[i].visibility === true) {
                    let id = String(i);
                    colors[id] = analysisModels[i].color;
                    colorsArr.push(analysisModels[i].color);
                }
            }
            if (chosenDateFrom < "2023-01")
                colorsArr.push("000000");
            let options = {
                title: "Średnia liczba osobników podczas obserwacji",
                legend: { position: "bottom" },
                colors: colorsArr
            };
            console.log("opts");
            console.log(options);
            setChartOptions(options);
        }
    }, [isLoading, analysisModels, appliedDateFrom, changedVisibility]);

    // parsing data needed to be visualised in chart
    useEffect(() => {
        if (modelsPredictions.length > 0) {
            let predictionsToVisualize = modelsPredictions.map(modelPrediction => {
                let modelNameWithId = modelPrediction.type + "#" + String(modelPrediction.id);
                let predictionToVisualize = {name: modelNameWithId}
                let regionsPredictions = [];
                modelPrediction.prediction.forEach(monthlyPrediction => {
                    monthlyPrediction.forEach(values => {
                        if (values[0] === chosenRegion) { // values[0] - region, values[1] - predicted value
                            regionsPredictions.push(values[1]);
                        }
                    });
                });
                predictionToVisualize.predictions = regionsPredictions;
                return predictionToVisualize;
            });

            const chosenRegionsTestData = [];

            const testMonths = Object.keys(chartTests);
            testMonths.forEach(month => {
                const places = Object.keys(chartTests[month]);
                places.forEach(place => {
                    if(place === chosenRegion) {
                        chosenRegionsTestData.push({month: month, value: chartTests[month][place]});
                    }
                });
            });

            const chartData = [];
            const chartFirstDataRow = ["Miesiące"];
            predictionsToVisualize.forEach(predictionToVisualize => {
                chartFirstDataRow.push(predictionToVisualize.name);
            })
            if(appliedDateFrom < "2023-01")
                chartFirstDataRow.push("Dane rzeczywiste");
            chartData.push(chartFirstDataRow);

            for (let i=0;i<chartMonths.length;i++) {
                const chartDataRow = [];
                chartDataRow.push(chartMonths[i]);
                predictionsToVisualize.forEach(predictionToVisualize => {
                    chartDataRow.push(predictionToVisualize.predictions[i]);
                });
                let testData = null;
                if(testMonths.includes(chartMonths[i])) {
                    chosenRegionsTestData.forEach(monthlyData => {
                        if(monthlyData.month === chartMonths[i]) {
                            testData = monthlyData.value;
                        }
                    })
                }
                if(appliedDateFrom < "2023-01")
                    chartDataRow.push(testData);
                chartData.push(chartDataRow);
            }

            setChartFinalData(chartData);
        }
    }, [chosenRegion, modelsPredictions, appliedDateFrom]); //[chartOptions, chosenRegion, modelsPredictions, appliedDateFrom]);

    // Filtering chart
    useEffect(() => {
        if (chartFinalData.length > 0) {

            let columnsToRemove = [];

            chartFinalData[0].forEach((header, index) => {
                console.log(header.substring(0, header.length-2));
                if(header.indexOf("#") !== -1) {
                    let id = header.substring(header.indexOf("#") + 1);
                    let isThisModelFiltered = false;
                    analysisModels.forEach(analysisModel => {
                       if(String(analysisModel.id) === id && analysisModel.visibility === true)
                           isThisModelFiltered = true;
                    });
                    if(!isThisModelFiltered) {
                        columnsToRemove.push(index);
                    }
                }
            });

            let filteredData = [];
            chartFinalData.forEach(singleRow => {
                let filteredRow = [];
                for (let i = 0; i < singleRow.length; i++) {
                    if (!columnsToRemove.includes(i)) {
                        filteredRow.push(singleRow[i]);
                    }
                }
                filteredData.push(filteredRow);
            });
            setChartFinalDataFiltered(filteredData);
            console.log("=========");
            console.log(chartOptions);
            console.log(analysisModels);
            console.log(chartFinalData);
            console.log(filteredData);
            console.log("=========");
        }
    }, [chosenRegion, chartOptions, analysisModels, chartFinalData, changedVisibility]);

    return (
        <div>
            <TopNav activePage={useLocation().pathname}/>
            <div className="columns-container">
                {isLoading && <div className="modal-info">Ładowanie...</div>}
                <div className="column-l-50 column-responsive-big">
                    <div className="column-content column-analysis-content small-screen-text-center">
                        <div className="chart-info-container">
                        <span className="map-header">Analiza modeli predykcji</span>
                        <span className="map-prediction-info">Wybrane Modele: </span>
                        <div className="models-container">
                            <ul className="models-list">
                                {analysisModels.map(analysisModel => (
                                    <li key={analysisModel.id}>
                                        <div className={analysisModel.visibility ? "model-block" : "model-block invisible-model-block"}>
                                            <div className="model-block-color" style={{backgroundColor: analysisModel.color}}></div>
                                            <div className={"model-name"}>
                                                <span>{analysisModel.type}</span>
                                                <div className={"model-additional-info"}>
                                                    <div>id: #{analysisModel.id}</div>
                                                    {analysisModel.defaultOptions
                                                        ? <div className={"model-additional-info-row"}>Standardowe opcje</div>
                                                        : <div>
                                                            {Object.keys(analysisModel).map( key =>
                                                                (key !== "color" && key !== "defaultOptions" && key !== "id" && key !== "type" && key !== "visibility")
                                                                && <div className={"model-additional-info-row"}>{key}: {analysisModel[key]}</div>
                                                            )}
                                                        </div>
                                                    }
                                                </div>
                                            </div>
                                            {analysisModel.visibility
                                                ? <div className="visibility-icon-container" onClick={() => {analysisModel.visibility = !analysisModel.visibility; setAnalysisModels(analysisModels); setChangedVisibility(!changedVisibility)}}><InvisibilityIcon/></div>
                                                : <div className="visibility-icon-container" onClick={() => {analysisModel.visibility = !analysisModel.visibility; setAnalysisModels(analysisModels); setChangedVisibility(!changedVisibility)}}><VisibilityIcon/></div>}
                                            <div className="x-button-slim-icon-container" onClick={() => {handleModelRemove(analysisModel.id); setChangedVisibility(!changedVisibility)}}><XbuttonSlim/></div>
                                        </div>
                                    </li>
                                ))}
                            </ul>
                        </div>
                        <span className="map-prediction-info">Wykres wyników wybranych modeli: </span>
                        <div className="plot-generate-submit-container">
                        <form onSubmit={handleSubmit}>
                            <input type="submit" value="Wygeneruj wykres"></input>
                        </form>
                            <div className="region-choice-container">
                                <label htmlFor="regions">Wykres dla województwa:</label>
                                <select id="regions" name="regions" onChange={e => setChosenRegion(e.target.value)}>
                                    <option value="małopolskie">małopolskie</option>
                                    <option value="lubuskie">lubuskie</option>
                                    {availableRegions.map(availableRegion =>
                                        <option value={availableRegion}>{availableRegion}</option>
                                    )}
                                </select>
                            </div>
                        </div>
                        </div>
                            {(!isLoading && chartFinalDataFiltered.length > 0 && chartFinalDataFiltered[0].length > 1) ? <Chart
                                chartType="LineChart"
                                className="chart"
                                data={chartFinalDataFiltered}
                                options={chartOptions}
                            />
                                :<div></div>
                            }
                    </div>
                </div>
                <div className="column-r-50 column-responsive-big">
                    <div className="column-l-50">
                        <div className="column-content analysis-options prediction-column border-r">
                            <div className="prediction-menu-container analysis-menu-container">
                                <a id="prediction-models-menu"></a>
                                <span
                                    className={(chosenModelsError || anyError) ? "form-error-label map-header" : "map-header"}>Modele predykcji:</span>
                                <form onSubmit={handleModelSubmit}>
                                    <ul className="prediction-menu model-menu">
                                        <li key='form-part-1'>
                                            <input type="submit" value="Dodaj model"></input>
                                            {chosenModelsError && <span className="form-error">{chosenModelsError}</span>}
                                        </li>
                                        <li key='form-part-2'>
                                            <label htmlFor="color-picker">Wybierz kolor:</label>
                                            <input type="color" value={chosenColor} id="color-picker" onChange={e => setChosenColor(e.target.value)}/>
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
                                                                <div key={predictionOption["option_name"]}>
                                                                    <div className='prediction-option-container'>
                                                                        <span className="form-default-label">{predictionOption["option_name"]}: </span>
                                                                        <span className="range-value">{chosenCustomOptions[predictionOption["option_type"]]}</span>
                                                                        <input type="range" name={predictionOption["option_type"]} id={predictionOption["option_type"]} min={predictionOption["option_min"]} max={predictionOption["option_max"]} defaultValue={predictionOption["option_default"]}
                                                                               onChange={e => handleRangeChange(e, 1)}/>
                                                                    </div>
                                                                </div>
                                                            )
                                                        }
                                                    </div>
                                                </div>
                                            }
                                        </li>
                                        <li key='form-part-4'>
                                            <span
                                                className={chosenModelError ? "form-error-label" : "form-default-label"}>Wybierz rodzaj predykcji:</span>
                                            {predictionTypes.length === 0 ?
                                                <div className='prediction-types-placeholder'>Zaznacz gatunek ptaka, aby
                                                    zobaczyć dostępne
                                                    modele</div> : predictionTypes.map(predictionType =>
                                                    <div key={predictionType.name}
                                                         className='prediction-type-container'>
                                                        <input type="radio" id={predictionType.name}
                                                               value={predictionType.name} name="prediction-type"
                                                               onChange={e => handleModelChange(e)}/>
                                                        <label className="radio-label"
                                                               htmlFor={predictionType.name}>{predictionType.text}</label>
                                                    </div>
                                                )}
                                            {chosenModelError && <span className="form-error">{chosenModelError}</span>}
                                        </li>
                                    </ul>
                                </form>
                            </div>
                        </div>
                    </div>
                    <div className="column-r-50">
                        <div className="column-content analysis-options prediction-column">
                            <div className="prediction-menu-container analysis-menu-container">
                                <a id="prediction-properties-menu"></a>
                                <span
                                    className={anyError ? "form-error-label map-header" : "map-header"}>Opcje predykcji:</span>
                                <form onSubmit={handleSubmit}>
                                    <ul className="prediction-menu">
                                        <li key='form-part-2'>
                                            <label
                                                className={chosenDateFromError ? "form-error-label" : "form-default-label"}
                                                htmlFor="prediction-date-from">Wybierz datę początkową predykcji</label>
                                            <input type="month" id="prediction-date-from" name="prediction-date-from"
                                                   onChange={e => handleDateFromChange(e)}/>
                                            {chosenDateFromError &&
                                                <span className="form-error">{chosenDateFromError}</span>}
                                            <label
                                                className={chosenDateToError ? "form-error-label" : "form-default-label"}
                                                htmlFor="prediction-date-to">Wybierz datę końcową predykcji</label>
                                            <input type="month" id="prediction-date-to" name="prediction-date-to"
                                                   onChange={e => handleDateToChange(e)}/>
                                            {chosenDateToError &&
                                                <span className="form-error">{chosenDateToError}</span>}
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
        </div>
    );
}

export default AnalysisPage;