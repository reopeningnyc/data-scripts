// call this with the returned result to end script
const done = arguments[0];

// define the function
const main = async () => {
  // next, get the workbook
  const workbook = window.hospitalizationViz.getWorkbook();

  // active the total hospital beds sheet
  const sheet = workbook.getActiveSheet();

  // get worksheet
  const worksheet = sheet.getWorksheets()[2];

  // get underlying data
  const raw = await worksheet.getUnderlyingDataAsync();

  // access actual data
  const data = raw.$0.$3;

  // return data
  return done(data);
};

main();
