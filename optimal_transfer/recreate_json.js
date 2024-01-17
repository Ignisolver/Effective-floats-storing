const AdmZip = require('adm-zip');
const fs = require('fs');
const struct = require('python-struct');
const axios = require("axios");


class ValuesExtractor {
    constructor() {
        this.valueMappings = new Map();
        this.valSetId = 0;
    }

    addValueMapping(key, replacementList) {
        this.valueMappings.set(key, { id: this.valSetId, replacementList });
        this.valSetId++;
    }

    replaceIntsWithLists(jsonObj) {
        this._manageObj(jsonObj);
        this.valSetId = 0;
    }

    _manageObj(obj) {
        if (Array.isArray(obj)) {
            this._manageList(obj);
        } else if (typeof obj === 'object') {
            this._manageDict(obj);
        }
    }

    _manageList(arr) {
        for (let i = 0; i < arr.length; i++) {
            this._manageObj(arr[i]);
        }
    }

    _manageDict(obj) {
        for (const key in obj) {
            if (key === 'values' && this.valueMappings.has(obj[key])) {
                const { id, replacementList } = this.valueMappings.get(obj[key]);
                obj[key] = id;
                if (replacementList) {
                    obj[key] = replacementList;
                }
            } else {
                this._manageObj(obj[key]);
            }
        }
    }
}

function saveToJsonFile(data, file_path) {
    const jsonDataString = JSON.stringify(data, null, 0);
    fs.writeFileSync(file_path, jsonDataString);
}

function processZipFile(zip_) {
    const extractedFiles = unzipAndReadZipFile(zip_);
    if (!extractedFiles) {
    console.error('Nie udało się uzyskać danych z pliku ZIP.');
    return null;
    }

    try {
    let jsonData = null;
    const floatArrays = {};
    for (const entryName in extractedFiles) {
        if (extractedFiles.hasOwnProperty(entryName)) {
        const fileContent = extractedFiles[entryName];
        const fileExtension = entryName.split('.').pop().toLowerCase();
        if (fileExtension === 'json') {
          jsonData = JSON.parse(fileContent.toString('utf-8'));
        } else if (fileExtension === 'bin') {
            const d_len = fileContent.length / 8
            const binaryData = struct.unpack('!'+d_len+'d', fileContent);
            floatArrays[entryName] = binaryData;
        }
        }
    }

    return { jsonData, floatArrays };
    } catch (error) {
    console.error('Błąd podczas przetwarzania danych:', error.message);
    return null;
    }
}

async function recreateJson(outputJsonPath, apiUrl, save=false) {
    try {
        const response = await axios.get(apiUrl, { responseType: 'arraybuffer' });
        const zipBuffer = Buffer.from(response.data);
        const admzip = new AdmZip(zipBuffer);
        const { jsonData, floatArrays } = processZipFile(admzip);
        const extractor = new ValuesExtractor();
        for (const key in floatArrays) {
            const floatArray = floatArrays[key];
            extractor.addValueMapping(parseInt(key), floatArray);
        }

        extractor.replaceIntsWithLists(jsonData);

        if (save){
            saveToJsonFile(jsonData, outputJsonPath);
        }
        console.log('JSON saved successfully.');
        return jsonData;
    } catch (error) {
        console.error('Error processing and saving JSON:', error.message);
    }
}

function unzipAndReadZipFile(zipFile) {
    try {
        const zipEntries = zipFile.getEntries();
        const extractedFiles = {};

        zipEntries.forEach((zipEntry) => {
        if (!zipEntry.isDirectory) {
            const fileContent = zipFile.readFile(zipEntry);
            extractedFiles[zipEntry.entryName] = fileContent;
        }
    });

    return extractedFiles;
    } catch (error) {
        console.error('Błąd podczas rozpakowywania pliku ZIP:', error.message);
        return null;
    }
}


const outputJsonPath = '..\\results\\restored_benchmark\\output.json';
const apiUrl = 'http://127.0.0.1:8000';

recreateJson(outputJsonPath, apiUrl, true).then(result => {
    console.log(result);
    })

