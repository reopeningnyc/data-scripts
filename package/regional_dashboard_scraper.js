// call this with the returned result to end script
const done = arguments[1];

// define a delay function
const delay = (ms) => new Promise((res) => setTimeout(res, ms));

// define the function
const main = async () => {
  // next, get the workbook
  const workbook = window.viz.getWorkbook();

  // get all sheets
  const sheets = workbook.getPublishedSheetsInfo().map((sheet) => {
    const { name, url, index } = sheet.$0;
    return { name, url, index };
  });

  // now identify the index of the desired sheet
  const hospIdx = sheets.find((sheet) => sheet.name.includes(arguments[0]))
    .index;

  // active the total hospital beds sheet
  const sheet = await workbook.activateSheetAsync(hospIdx);

  // switch to NYC
  document
    .querySelector("iframe")
    .contentWindow.document.querySelector("a.FIText[title='New York City']")
    .parentElement.childNodes[0].click();

  // wait 2 seconds before doing the next thing
  await delay(2000);

  // get worksheet
  const worksheet = sheet.getWorksheets()[13];

  // get underlying data
  const raw = await worksheet.getUnderlyingDataAsync();

  console.log(raw);

  // access actual data
  const data = raw.$0.$3;

  // return data
  return done(data);
};

main();
