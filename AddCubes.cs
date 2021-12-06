using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class AddCubes : MonoBehaviour {

  public TextAsset mapData;
 	public GameObject Wall;

	// Use this for initialization
	void Start () {

    string mapDataStr = mapData.text;
    string[] parsed = mapDataStr.Split('\n');
    List<int> listX = new List<int>();
    List<int> listY = new List<int>();
    for (int i = 0; i < parsed.Length-1; i++ ) {
        string[] tempXY = parsed[i].Split(' ');
        string tempXStr = tempXY[0];
        string tempYStr = tempXY[1];
        int tempX = Int32.Parse(tempXStr);
        int tempY = Int32.Parse(tempYStr);
        listX.Add(tempX);
        listY.Add(tempY);
    }
    for (int i = 0; i < listX.Count; i++) {
      Instantiate(Wall, new Vector3(listX[i],2,listY[i]), Quaternion.identity);


    }
//    for (int y = 0; y < 5; y++) {
//      for (int x = 0; x < 5; x++) {
//        Instantiate(Wall, new Vector3(x, y, 0), Quaternion.identity);
//      }
//    }
	}

	// Update is called once per frame
	void Update () {

	}
}
