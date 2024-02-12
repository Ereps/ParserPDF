// Test JS

const cpdf = require("pdf.js-extract").PDFExtract;
const fs = require('fs');
const PDFExtract = new cpdf();
const options = {};
const pathDir = "ParserPDF/Corpus_test/"

fs.readdirSync(pathDir).forEach(filename => {
    if (filename.substring(filename.indexOf('.')+1, filename.length) == "pdf") {
        PDFExtract.extract(pathDir+filename, options, (err, data) => {
            if (err) return console.log(err);
            var title = data.meta.info.Title;
            var authors = data.meta.info.Author;
            console.log("Filename:  " + filename)
            console.log("Title:     " + title);
            console.log("Authors:   " + authors);
            console.log(data.pages);
            console.log();
        });
    }
})

