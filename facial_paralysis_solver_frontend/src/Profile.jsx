import React, { useState, useEffect } from "react";
import Webcam from "react-webcam";
import { TailSpin } from "react-loader-spinner";
import Chart from "./Chart";

const videoConstraints = {
  width: 400,
  height: 400,
  facingMode: "user",
};
const Profile = () => {
  const [picture, setPicture] = useState("");
  const [newPicture, setNewPicture] = useState("");
  const [landmark, setlandmark] = useState("");
  const [compare, setCompare] = useState(false);
  const [score, setScore] = useState(-1000);
  const [newLandmark, setNewLandmark] = useState("");
  const [loadings, setLoadings] = useState(false);
  const [message, setMessage] = useState("");
  const [currentImage, setCurrentImage] = useState(0);
  const [imgUrl, setImgUrl] = useState("");
  const webcamRef = React.useRef(null);
  const [images, setImages] = useState([]);
  const capture = React.useCallback(() => {
    const screenshot = webcamRef.current.getScreenshot();
    setLoadings(true);
    setPicture(screenshot);
  });
  // send the captured image to the server
  useEffect(() => {
    if (picture) {
      const formData = new FormData();
      formData.append("image", picture);
      fetch("http://127.0.0.1:5000/upload", {
        method: "POST",
        body: formData,
      })
        .then((response) => response.json())
        .then((data) => {
          setLoadings(false);
          console.log(data);
          setImages([
            data.img1,
            data.img2,
            data.img3,
            data.img4,
            data.img5,
            data.img6,
            data.img7,
            data.img8,
            data.img9,
            data.img10,
            data.img11,
            data.img12,
            data.img13,
            data.img14,
            data.img15,
            data.img16,
          ]);
          setlandmark(data);
        })
        .catch((error) => {
          console.error(error);
        });
    }
  }, [picture]);

  const sendImageAndLandmark = () => {
    const screenshot = webcamRef.current.getScreenshot();
    setLoadings(true);
    setNewPicture(screenshot);
  };

  useEffect(() => {
    if (newPicture) {
      const formData = new FormData();
      formData.append("image", newPicture);
      formData.append("landmark", JSON.stringify(landmark));
      fetch("http://127.0.0.1:5000/compare", {
        method: "POST",
        body: formData,
      })
        .then((response) => response.json())
        .then((data) => {
          //   console.log(data);
          setLoadings(false);
          setScore(data.score / 3);
          //   setImgUrl(images[currentImage]);
          //   setNewLandmark(data);
        })
        .catch((error) => {
          console.error(error);
        });
    }
  }, [newPicture]);

  useEffect(() => {
    if (score >= 80) {
      setMessage("Success!!!");
      console.log(currentImage);
      setCurrentImage(currentImage + 1);
    } else if (score < 80 && score > -100) {
      setMessage("Try again!!!");
    } else {
      setMessage("");
    }
  }, [score]);

  useEffect(() => {
    if (currentImage === 16) {
      setMessage("You have completed the task!!!");
      setScore(0);
    }
  }, [currentImage]);

  console.log(currentImage);

  return (
    <div className="flex flex-col justify-center items-center reletive">
      {loadings && (
        <div className="absolute top-1/2 left-1/2 z-10 -translate-x-1/2 -translate-y-1/2">
          <TailSpin
            height="80"
            width="80"
            color="#4fa94d"
            ariaLabel="tail-spin-loading"
            radius="1"
            wrapperStyle={{}}
            wrapperClass=""
            visible={true}
          />
        </div>
      )}
      <h2 className="text-center text-4xl mb-5">Photo Capture</h2>

      {score > 0 && <h1>{score}</h1>}
      {message && <h1>{message}</h1>}
      <div className="relative mb-5">
        <Webcam
          audio={false}
          height={400}
          ref={webcamRef}
          width={400}
          screenshotFormat="image/jpeg"
          videoConstraints={videoConstraints}
          mirrored={true}
          className=""
        />
        {landmark && (
          <Chart landmark={landmark} color={"#fff"} id={currentImage} />
        )}
        {/* {newLandmark && (
          <Chart landmark={newLandmark} color={"#8884d8"} id={0} />
        )} */}
      </div>
      <div>
        {compare ? (
          <button
            onClick={(e) => {
              e.preventDefault();
              sendImageAndLandmark();
            }}
            className="z-10"
          >
            compare
          </button>
        ) : (
          <button
            onClick={(e) => {
              e.preventDefault();
              capture();
              setCompare(true);
            }}
            className="btn btn-danger"
          >
            Capture
          </button>
        )}
        <h2>{currentImage}/16 Completed</h2>
      </div>
    </div>
  );
};
export default Profile;
