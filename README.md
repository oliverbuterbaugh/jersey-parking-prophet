# jersey-parking-prophet

## Intro

This is a simple random forest core ml model to predict car park availability in six Jersey car parks. I've trained it on data collected every 5 minutes for only 3 weeks, so it'll be nowhere near production-ready until it has months more data. That being said, it's already picked up unique trends in different carparks, such as the exothermic behaviour of Minden Pl before the work day, so as a guide and proof of concept it works well. 

## Data collection

Government of Jersey publishes the live data of Green St, Minden Pl, Patriotic St, Sand St, Pier Rd, and Les Jardin carparks to https://www.gov.je/Travel/Motoring/Parking/pages/carparkspaces.aspx, which, on brief inspection of the source, gets its data from the public API https://sojpublicdata.blob.core.windows.net/sojpublicdata/carpark-data.json. I've included the script which has been pulling from here every 5 minutes.

## Usage in Xcode project / app playground

Drag the .mlpackage file into the sidebar, ensuring it's added to the target. On build, a class for the model will be automatically generated. You can then make a simple call to the model using the built-in input object.

```
import CoreML

let model = try CarvoyantWeather(configuration: MLModelConfiguration())

let input = CarvoyantWeatherInput(
    Precipitation: 0.0, // 0 mm rainfall
    WindSpeed: 20.0, // 20 km/h windspeed
    DayOfWeek: 0, // monday
    MinutesPastMidnight: 600, // 10:00 am
    CarparkCodeInt: 5, // Les Jardin
    WeekdayWeekend: 1, // weekend
    TimeOfDay: 1 // within working hours
)

let result = try model.prediction(input: input)
print(Int(result.Available_Spaces))
```

For an app playground, which doesn't support .mlmodel resources and therefore won't generate the model class, just use a dummy Xcode project to build and generate the class, then copy it into your app playground. Change the urlOfModelInThisBundle class to this in order to get it working on the iPad Playground app:
```
class var urlOfModelInThisBundle : URL {
  let resPath = Bundle(for: self).url(forResource: "CarvoyantWeather", withExtension: "mlmodel")!
  return try! MLModel.compileModel(at: resPath)
}
```

