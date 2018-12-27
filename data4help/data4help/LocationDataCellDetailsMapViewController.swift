//
//  LocationDataCellDetailsMapViewController.swift
//  data4help
//
//  Created by Alessandro Nichelini on 27/12/2018.
//  Copyright © 2018 Francesco Peressini. All rights reserved.
//

import UIKit
import MapKit
import os.log

class LocationDataCellDetailsMapViewController: UIViewController {

    @IBOutlet weak var mapView: MKMapView!
    
    var latitude: Double = 0.0
    var longitude: Double = 0.0
    
    func mapView(_ mapView: MKMapView, viewFor annotation: MKAnnotation) -> MKAnnotationView? {
        guard annotation is MKPointAnnotation else { return nil }
        
        let identifier = "Annotation"
        var annotationView = mapView.dequeueReusableAnnotationView(withIdentifier: identifier)
        
        if annotationView == nil {
            annotationView = MKPinAnnotationView(annotation: annotation, reuseIdentifier: identifier)
            annotationView!.canShowCallout = true
        } else {
            annotationView!.annotation = annotation
        }
        
        return annotationView
    }
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        let position = MKPointAnnotation()
        position.title = "Your past position"
        position.coordinate = CLLocationCoordinate2D(latitude: latitude, longitude: longitude)
        mapView.addAnnotation(position)
        mapView.setCenter(position.coordinate, animated: true)
        mapView.reloadInputViews()
    }

}
