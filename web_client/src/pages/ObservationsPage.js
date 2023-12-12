import TopNav from "../components/TopNav";
import {Chart} from "react-google-charts";
import {useState, useEffect} from "react";
import source from "../backendConfig";
import {useLocation} from "react-router-dom";
import dayjs from "dayjs";
import {DatePicker} from "@mui/x-date-pickers";

let data = [
    [["Region", "Bird encounters"],
        ["USA", 100]]

];

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

    function handleDateFromChange(value) {
        setChosenDateFrom(dayjs(value).format('YYYY-MM-DD'));
    }

    function handleDateToChange(value) {
        setChosenDateTo(dayjs(value).format('YYYY-MM-DD'));
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

        setIsLoading(true);
        await fetch(url)
            .then(response => response.json())
            .then(data => {
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

    const [birdSpecies, setBirdSpecies] = useState([]);
    const [filteredBirdSpecies, setFilteredBirdSpecies] = useState([]);
    // Form variables
    const [chosenBirdCommonName, setChosenBirdCommonName] = useState("");
    const [chosenBirdScientificName, setChosenBirdScientificName] = useState("");
    const [chosenDateFrom, setChosenDateFrom] = useState("");
    const [chosenDateTo, setChosenDateTo] = useState("");
    // Form error information
    const [chosenBirdScientificNameError, setChosenBirdScientificNameError] = useState("");
    const [chosenDateFromError, setChosenDateFromError] = useState("");
    const [chosenDateToError, setChosenDateToError] = useState("");
    const [anyError, setAnyError] = useState("");

    // Prediction visualization
    const [predictionData, setPredictionData] = useState(data);
    const [predictionSpecies, setPredictionSpecies] = useState("");
    const [isLoading, setIsLoading] = useState(false);
    const [mapOptions, setMapOptions] = useState({
        region: "PL",
        displayMode: "regions",
        resolution: "provinces",
        colorAxis: {minValue: 0, maxValue: 0, colors: ["#ffffff", "#ff0000"]}
    });

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
                                   data={predictionData[0]} options={mapOptions}/>
                        </div>
                        <div className="map-info-container">
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
                                        <input type="submit" value="Sprawdź obserwacje"></input>
                                    </li>
                                    <li key='form-part-2'>
                                        <label
                                            className={chosenDateFromError ? "form-error-label" : "form-default-label"}
                                            htmlFor="prediction-date-from">Wybierz datę początkową okresu
                                            obserwacji</label>
                                        <div className="pg-custom-mui-input"><DatePicker views={['day', 'month', 'year']} onChange={(v) => handleDateFromChange(v)}
                                                                                         slotProps={{
                                                                                             field:{
                                                                                                 id:'prediction-date-from'
                                                                                             }
                                                                                         }} /></div>
                                        {chosenDateFromError &&
                                            <span className="form-error">{chosenDateFromError}</span>}
                                        <label className={chosenDateToError ? "form-error-label" : "form-default-label"}
                                               htmlFor="prediction-date-to">Wybierz datę końcową okresu
                                            obserwacji</label>
                                        <div className="pg-custom-mui-input">
                                            <DatePicker views={['day', 'month', 'year']}
                                                        onChange={(v) => handleDateToChange(v)}
                                                        slotProps={{
                                                            field:{
                                                                id:'prediction-date-to'
                                                            }
                                            }} />
                                        </div>
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

export default ObservationsPage;