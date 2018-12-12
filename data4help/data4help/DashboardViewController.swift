import Alamofire
import UIKit
import HealthKit

let healthKitStore: HKHealthStore = HKHealthStore()

class DashboardViewController: UIViewController {
    
    @IBOutlet weak var age: UILabel!
    @IBOutlet weak var heart: UILabel!
    
    @IBAction func updateButton(_ sender: Any) {
        let (age, bloodType) = readData()
        self.age.text = "\(String(age!))"
        
        //Reading BPM
        self.readMostRecentSample()
    }
    
    @IBAction func authorize(_ sender: Any) {
        self.authorizeHealthKitInApp()
    }
    
    func readData() -> (age:Int?, bloodType:HKBloodTypeObject?) {
        
        var age:Int?
        var bloodType:HKBloodTypeObject?
        
        //Reading the date of birth
        do {
            let birthday = try healthKitStore.dateOfBirthComponents()
            let currentYear = Calendar.current.component(.year, from: Date())
            age = currentYear - birthday.year!
        } catch {}
        
        //Reading the blood type
        do {
            bloodType = try healthKitStore.bloodType()
        } catch {}
        
        return (age, bloodType)
        
    }
    
    func readMostRecentSample() {
        
        let BPM = HKSampleType.quantityType(forIdentifier: HKQuantityTypeIdentifier.heartRate)
        
        let query = HKSampleQuery(sampleType: BPM!, predicate: nil, limit: HKObjectQueryNoLimit, sortDescriptors: nil) { (query, results, error) in
            if let result = results?.last as? HKQuantitySample {
                print("BPM = \(result.quantity)")
                DispatchQueue.main.async(execute: { () -> Void in
                    self.heart.text = "\(result.quantity)"
                })
            }
        }
    }
    
    func authorizeHealthKitInApp() {
        
        let healthKitTypeToRead: Set<HKObjectType> = [
            HKObjectType.characteristicType(forIdentifier: HKCharacteristicTypeIdentifier.dateOfBirth)!,
            HKObjectType.characteristicType(forIdentifier: HKCharacteristicTypeIdentifier.bloodType)!,
            HKObjectType.quantityType(forIdentifier: HKQuantityTypeIdentifier.heartRate)!,
        ]
        
        let healthKitTypeToWrite: Set<HKSampleType> = []
        
        if !HKHealthStore.isHealthDataAvailable() {
            print("Data not available")
            return
        }
        
        healthKitStore.requestAuthorization(toShare: healthKitTypeToWrite, read: healthKitTypeToRead) { (success, error) -> Void in
            UserDefaults.standard.set(true, forKey: "healthToggleStatus")
            print("Read & Write authorization acquired!")
        }
        
    }
    
    @IBAction func updateAndUpload(_ sender: UIButton) {
        print("click")
        subscribeToHeartBeatChanges()
    }
    
    public func subscribeToHeartBeatChanges() {
        
        // Creating the sample for the heart rate
        guard let sampleType: HKSampleType =
            HKObjectType.quantityType(forIdentifier: .heartRate) else {
                return
        }
        
        /// Creating an observer, so updates are received whenever HealthKit’s
        // heart rate data changes.
        let heartRateQuery = HKObserverQuery.init(
            sampleType: sampleType,
            predicate: nil) { [weak self] _, _, error in
                guard error == nil else {
                    print("error!")
                    return
                }
                
                /// When the completion is called, an other query is executed
                /// to fetch the latest heart rate
                self?.fetchLatestHeartRateSample(completion: { sample in
                    guard let sample = sample else {
                        return
                    }
                    
                    /// The completion in called on a background thread, but we
                    /// need to update the UI on the main.
                    DispatchQueue.main.async {
                        
                        /// Converting the heart rate to bpm
                        let heartRateUnit = HKUnit(from: "count/min")
                        let heartRate = sample
                            .quantity
                            .doubleValue(for: heartRateUnit)
                        
                        /// Updating the UI with the retrieved value
                        print("\(Int(heartRate))")
                    }
                })
        }
    }
    
<<<<<<< Updated upstream
=======
    public func fetchLatestHeartRateSample(
        completion: @escaping (_ sample: HKQuantitySample?) -> Void) {
        
        /// Create sample type for the heart rate
        guard let sampleType = HKObjectType.quantityType(forIdentifier: .heartRate) else {
                completion(nil)
                return
        }
        
        print("fatto 1")
        
        /// Predicate for specifiying start and end dates for the query
        let predicate = HKQuery
            .predicateForSamples(
                withStart: Date.distantPast,
                end: Date(),
                options: .strictEndDate)
        
        /// Set sorting by date.
        let sortDescriptor = NSSortDescriptor(
            key: HKSampleSortIdentifierStartDate,
            ascending: false)
        
        /// Create the query
        let query = HKSampleQuery(
            sampleType: sampleType,
            predicate: predicate,
            limit: Int(HKObjectQueryNoLimit),
            sortDescriptors: [sortDescriptor]) { (_, results, error) in
                
                guard error == nil else {
                    print("Error: \(error!.localizedDescription)")
                    return
                }
                
                completion(results?[0] as? HKQuantitySample)
        }
        
        healthStore.execute(query)
    }
    //@IBOutlet weak var totalSteps: UILabel!
    
>>>>>>> Stashed changes
    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view.
    }
<<<<<<< Updated upstream
    
    
    
=======
>>>>>>> Stashed changes
}
