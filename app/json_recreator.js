const fs = require('fs');
const path = require('path');
const struct = require('python-struct');

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
                obj[key] = replacementList;
            } else {
                this._manageObj(obj[key]);
            }
        }
    }
}

function readFloatsFromFile(file_path) {
    const file_content = fs.readFileSync(file_path);
    const unpacked_data = struct.unpack('!' + file_content.length / 8 + 'd', file_content);
    return unpacked_data;
}

function readMetadataFile(metadata_path) {
    const metadata_content = fs.readFileSync(metadata_path, 'utf-8');
    return JSON.parse(metadata_content);
}

function readDataFromFolder(folder_path) {
    const metadataPath = path.join(folder_path, "..")
    const jsonDataPath = path.join(metadataPath, 'metadata.json');
    const jsonData = readMetadataFile(jsonDataPath);

    const floatArrays = {};

    fs.readdirSync(folder_path).forEach(file => {
        if (file.endsWith('.bin')) {
            const key = path.basename(file, '.bin');
            const file_path = path.join(folder_path, file);
            const floatArray = readFloatsFromFile(file_path);
            floatArrays[key] = floatArray;
        }
    });

    return { jsonData, floatArrays };
}

function saveToJsonFile(data, file_path) {
    const jsonDataString = JSON.stringify(data, null, 0);
    fs.writeFileSync(file_path, jsonDataString);
}

// Przykład użycia:
// const folderPath = 'C:\\STUDIA\\LSC\\PROJ\\Effective-floats-storing\\results\\restored_benchmark\\struct_packed';
const folderPath = 'path_to_struct_packed_folder';
// metadata.json file should be in the folder above
const outputJsonPath = path.join(folderPath, 'output.json');

const { jsonData, floatArrays } = readDataFromFolder(folderPath);

// Mierzymy czas rozpoczęcia operacji
const startTime = performance.now();

const extractor = new ValuesExtractor();

// Dodaj floatArrays jako mapowanie klucz-int
for (const key in floatArrays) {
    const floatArray = floatArrays[key];
    extractor.addValueMapping(parseInt(key), floatArray);
}

// Zamień inty na listy floatów w obiekcie JSON
extractor.replaceIntsWithLists(jsonData);

// Mierzymy czas zakończenia operacji
const endTime = performance.now();

// Zapisz wynikowy obiekt jsonData do pliku JSON
saveToJsonFile(jsonData, outputJsonPath);
console.log(`Wynik zapisany do pliku: ${outputJsonPath}`);

// Wyświetl czas wykonania operacji
console.log(`Czas wykonania: ${endTime - startTime} milisekundy`);