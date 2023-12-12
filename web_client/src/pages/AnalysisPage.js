import TopNav from "../components/TopNav";
import XbuttonSlim from "../components/svg/XbuttonSlim";
import {Chart} from "react-google-charts";
import {useState, useEffect} from "react";
import source from "../backendConfig";
import {useLocation} from "react-router-dom";
import VisibilityIcon from "../components/svg/VisiblityIcon";
import InvisibilityIcon from "../components/svg/InvisibiltyIcon";
import {DatePicker} from "@mui/x-date-pickers";
import dayjs from "dayjs";
import {Slider, NativeSelect} from "@mui/material";

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


let DEFAULT_PLOT_COLOR = "#FF0000";

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
    }

    function handleRangeChange(event) {
        setSliderChange(-sliderChange);
        let optionRanges = chosenCustomOptions;
        optionRanges[event.target.name] = event.target.value;
        setChosenCustomOptions(optionRanges);
    }

    function handleModelChange(event, textName) {
        setChosenModel(event.target.value);
        setChosenModelName(textName);
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
            delete customOptions.name;
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
            let url;
            if (!analysisModel.defaultOptions) {
                url = `${source}birds/${chosenBirdScientificName}/models/${analysisModel.type}/predict?from=${chosenDateFrom}&to=${chosenDateTo}${optionParms}&edge=2021-12`;
            } else {
                url = `${source}birds/${chosenBirdScientificName}/models/${analysisModel.type}/predict?from=${chosenDateFrom}&to=${chosenDateTo}&edge=2021-12`;
            }

            return fetch(url)
                .then(response => response.json())
                .then(data => {
                    let dataPlaceholder = data.predictions; // change dataPlaceholder to another name
                    let wholePrediction = [];
                    let maxPredictionValue = 0;
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
                    let generatedModelPredictionWithInfo = {"prediction": wholePrediction, "type": analysisModel.type, "id": analysisModel.id, "name": analysisModel.name};
                    return generatedModelPredictionWithInfo;
                })
                .catch(error => console.error(error));
        }))
            .then(predictions => {
                setAppliedDateFrom(chosenDateFrom);
                return predictions;
            })
            .then(predictions => predictions.map(prediction => {
                allModelsPredictions = [...allModelsPredictions, prediction];
            }))
            .then(p => {
                setModelsPredictions(allModelsPredictions)
                if (allModelsPredictions.length > 0 && allModelsPredictions[0].prediction.length > 0) {
                    const regionsOfPrediction = [];
                    allModelsPredictions[0].prediction[0].forEach(regionPrediction => {
                        if (regionPrediction[0] !== "Region") {
                            regionsOfPrediction.push(regionPrediction[0]);
                        }
                    });
                    setPredictedRegions(regionsOfPrediction);
                }
            })
            .catch(error => console.error(error));
        setIsLoading(false);
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
        modelsInfo["name"] = chosenModelName;
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

    const [sliderChange, setSliderChange] = useState(1);

    const [predictionTypes, setPredictionTypes] = useState([]);
    const [birdSpecies, setBirdSpecies] = useState([]);
    const [filteredBirdSpecies, setFilteredBirdSpecies] = useState([]);
    const [predictionOptions, setPredictionOptions] = useState([]);
    // Analysis variables
    const [analysisModels, setAnalysisModels] = useState([]);
    const [currentModelId, setCurrentModelId] = useState(0);
    const [changedVisibility, setChangedVisibility] = useState(false);
    const [availableRegions, setAvailableRegions] = useState([...regionsPlaceHolder]);
    const [predictedRegions, setPredictedRegions] = useState([...regionsPlaceHolder]);
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
    const [chosenModelName, setChosenModelName] = useState("");
    const [chosenDateFrom, setChosenDateFrom] = useState("");
    const [chosenDateTo, setChosenDateTo] = useState("");
    const [chosenColor, setChosenColor] = useState(DEFAULT_PLOT_COLOR);
    const [defaultOptions, setDefaultOptions] = useState(true);
    const [chosenCustomOptions, setChosenCustomOptions] = useState({});
    // Form error information
    const [chosenBirdScientificNameError, setChosenBirdScientificNameError] = useState("");
    const [chosenModelError, setChosenModelError] = useState("");
    const [chosenDateFromError, setChosenDateFromError] = useState("");
    const [chosenDateToError, setChosenDateToError] = useState("");
    const [chosenModelsError, setChosenModelsError] = useState("");
    const [anyError, setAnyError] = useState("");

    // Prediction visualization
    const [optionNamesDictionary, setOptionNamesDictionary] = useState({});
    const [modelsPredictions, setModelsPredictions] = useState([]);
    const [isLoading, setIsLoading] = useState(false);

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
                    let opts = optionNamesDictionary;
                    let chosenOptions = {};
                    const optionNames = Object.keys(options);
                    optionNames.forEach(optionName => {
                        availableOptions.push({option_type: optionName, option_name: options[optionName]["pl_name"],
                            option_default: options[optionName]["default"], option_max: options[optionName]["max"], option_min: options[optionName]["min"]});
                        chosenOptions[optionName] = options[optionName]["default"];
                        opts[optionName] = options[optionName]["pl_name"];
                    });
                    setPredictionOptions(availableOptions);
                    setChosenCustomOptions(chosenOptions);
                    setOptionNamesDictionary(opts);
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
                if(chartFinalDataFiltered.length > 0) {
                    if(!chartFinalDataFiltered[0].includes(analysisModels[i].name + "#" + analysisModels[i].id)) {
                        continue;
                    }
                }
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
            setChartOptions(options);
        }
    }, [isLoading, analysisModels, appliedDateFrom, changedVisibility, chartFinalDataFiltered]);

    // parsing data needed to be visualised in chart
    useEffect(() => {
        if (modelsPredictions.length > 0) {
            let predictionsToVisualize = modelsPredictions.map(modelPrediction => {
                let modelNameWithId = modelPrediction.name + "#" + String(modelPrediction.id);
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
        }
    }, [chosenRegion, analysisModels, chartFinalData, changedVisibility]);

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
                                                <span>{analysisModel.name}</span>
                                                <div className={"model-additional-info"}>
                                                    <div>id: #{analysisModel.id}</div>
                                                    {analysisModel.defaultOptions
                                                        ? <div className={"model-additional-info-row"}>Standardowe opcje</div>
                                                        : <div>
                                                            {Object.keys(analysisModel).map( key =>
                                                                (key !== "name" && key !== "color" && key !== "defaultOptions" && key !== "id" && key !== "type" && key !== "visibility")
                                                                && <div className={"model-additional-info-row"}>{optionNamesDictionary[key]}: {analysisModel[key]}</div>
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
                                <div className="pg-custom-mui-input">
                                    <NativeSelect id="regions" onChange={e => setChosenRegion(e.target.value)}>
                                        {availableRegions.map(availableRegion =>
                                            <option value={availableRegion}>{availableRegion}</option>
                                        )}
                                    </NativeSelect>
                                </div>
                            </div>
                        </div>
                        </div>
                            {(!isLoading && chartFinalDataFiltered.length > 0 && chartFinalDataFiltered[0].length > 1 && predictedRegions.includes(chosenRegion))
                                ? <Chart
                                chartType="LineChart"
                                className="chart"
                                data={chartFinalDataFiltered}
                                options={chartOptions}
                            />
                                :<div></div>
                            }
                            {(!isLoading && chartFinalDataFiltered.length > 0 && chartFinalDataFiltered[0].length > 1 && !predictedRegions.includes(chosenRegion))
                                ? <div><span className={"form-error"}>Brak danych</span></div>
                                :<div></div>
                            }
                    </div>
                </div>
                <div className="column-r-50 column-responsive-big">
                    <div className="column-l-50">
                        <div className="column-content analysis-options prediction-column border-r">
                            <div className="prediction-menu-container analysis-menu-container">
                                <span id="prediction-models-menu"
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
                                                               onChange={e => handleModelChange(e, predictionType.text)}/>
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
                                <span id="prediction-properties-menu"
                                    className={anyError ? "form-error-label map-header" : "map-header"}>Opcje predykcji:</span>
                                <form onSubmit={handleSubmit}>
                                    <ul className="prediction-menu">
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
                                            <label
                                                className={chosenDateToError ? "form-error-label" : "form-default-label"}
                                                htmlFor="prediction-date-to">Wybierz datę końcową predykcji</label>
                                            <div className="pg-custom-mui-input"><DatePicker views={['month', 'year']} onChange={(v) => handleDateToChange(v)}
                                                                                             slotProps={{
                                                                                                 field:{
                                                                                                     id:'prediction-date-to'
                                                                                                 }
                                                                                             }} /></div>
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
        </div>
    );
}

export default AnalysisPage;