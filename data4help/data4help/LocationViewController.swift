//
//  LocationViewController.swift
//  data4help
//
//  Created by Francesco Peressini on 23/12/2018.
//  Copyright © 2018 Francesco Peressini. All rights reserved.
//

import Alamofire
import UIKit
import CoreLocation
import MapKit

class LocationViewController: UIViewController, CLLocationManagerDelegate {
    
    let locationManager = CLLocationManager()
    let LOCATION_POST_URL = Global.getUserURL() + Global.LOCATION_POST
    
    @IBOutlet weak var map: MKMapView!
    
    override func viewDidLoad() {
        super.viewDidLoad()
        if CLLocationManager.locationServicesEnabled() {
            switch CLLocationManager.authorizationStatus() {
            case .notDetermined, .restricted, .denied:
                let alert = UIAlertController(title: "Attention!", message: "Authorization required", preferredStyle: .alert)
                alert.addAction(UIAlertAction(title: "OK", style: .cancel, handler: nil))
                self.present(alert, animated: true)
            case .authorizedAlways, .authorizedWhenInUse:
                locationManager.delegate = self
                locationManager.desiredAccuracy = kCLLocationAccuracyBest
                locationManager.requestAlwaysAuthorization()
                locationManager.startUpdatingLocation()
                locationManager.distanceFilter = 250
            }
        }
        else {
            let alert = UIAlertController(title: "Attention!", message: "Location services not enabled", preferredStyle: .alert)
            alert.addAction(UIAlertAction(title: "OK", style: .cancel, handler: nil))
            self.present(alert, animated: true)
        }
        
    }
    
    func locationManager(_ manager: CLLocationManager, didUpdateLocations locations: [CLLocation]) {
        let location = locations[0]     //most recent position of the user
        let latitude = location.coordinate.latitude
        let longitude = location.coordinate.longitude
        
        let span: MKCoordinateSpan = MKCoordinateSpan.init(latitudeDelta: 0.01, longitudeDelta: 0.01)
        let myLocation: CLLocationCoordinate2D = CLLocationCoordinate2DMake(location.coordinate.latitude, location.coordinate.longitude)
        let region: MKCoordinateRegion = MKCoordinateRegion.init(center: myLocation, span: span)
        map.setRegion(region, animated: true)
        self.map.showsUserLocation = true
        
        for loc in locations {
         print(loc)
         }
        
        /*let parameters: Parameters = [
            "latitude": latitude,
            "longitude": longitude,
            ]
        
        Alamofire.request(LOCATION_POST_URL, method: .post, parameters: parameters, encoding: JSONEncoding.default)
            .responseJSON { response in
            
        }*/
        
    }
    
}
