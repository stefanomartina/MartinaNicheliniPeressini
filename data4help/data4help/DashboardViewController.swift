import Alamofire
import UIKit
import HealthKit

func queryHealhkit() -> [Double] {
    var toReturn: [Double] = []
    
    let heartRateUnit:HKUnit = HKUnit(from: "count/min")
    let heartRateType:HKQuantityType   = HKQuantityType.quantityType(forIdentifier: HKQuantityTypeIdentifier.heartRate)!
    var heartRateQuery:HKSampleQuery?
    
    let calendar = Calendar.current
    let now = Date()
    let components = calendar.dateComponents([.year,.month,.day], from: now)
    
    guard let startDate = calendar.date(from: components) else {
        fatalError("*** Unable to create the start date ***")
    }
    
    let endDate = calendar.date(byAdding: .day, value: 1, to: startDate)
    
    guard let sampleType = HKSampleType.quantityType(forIdentifier: HKQuantityTypeIdentifier.heartRate) else
    { fatalError("*** This method should never fail ***") }
    
    let predicate = HKQuery.predicateForSamples(withStart: startDate, end: endDate)
    
    
    let query = HKSampleQuery(sampleType: sampleType, predicate: predicate, limit: Int(HKObjectQueryNoLimit), sortDescriptors: nil) {
        query, results, error in
        
        let samples = results as! [HKQuantitySample]
        
        for sample in samples {
            toReturn.append(sample.quantity.doubleValue(for: heartRateUnit))
        }
    }
    healthStore.execute(query)
    return toReturn
}

class DashboardViewController: UIViewController {

    @IBAction func updateAndUpload(_ sender: UIButton) {
        var returned: [Double] = queryHealhkit()
    }
    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view.
    }
    
}
