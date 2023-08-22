import React from "react";
import { zip } from "lodash";
import { ScatterChart, Scatter, XAxis, YAxis, ZAxis } from "recharts";

const Chart = ({ landmark, color, id = 0 }) => {
//   console.log(id, color);
  const x = [
    landmark.x1,
    landmark.x2,
    landmark.x3,
    landmark.x4,
    landmark.x5,
    landmark.x6,
    landmark.x7,
    landmark.x8,
    landmark.x9,
    landmark.x10,
    landmark.x11,
    landmark.x12,
    landmark.x13,
    landmark.x14,
    landmark.x15,
    landmark.x16,
  ];
  const y = [
    landmark.y1,
    landmark.y2,
    landmark.y3,
    landmark.y4,
    landmark.y5,
    landmark.y6,
    landmark.y7,
    landmark.y8,
    landmark.y9,
    landmark.y10,
    landmark.y11,
    landmark.y12,
    landmark.y13,
    landmark.y14,
    landmark.y15,
    landmark.y16,
  ];
  const data = zip(x[id], y[id]).map(([x, y]) => ({ x, y }));
  //   console.log(data);
  // Create the chart options
  const options = {
    // Set the background color to transparent
    backgroundColor: "rgba(0, 0, 0, 0)",
  };

  return (
    <div className="absolute top-[5%] left-[%]">
      <ScatterChart width={350} height={350}>
        <XAxis type="number" dataKey="x" hide />
        <YAxis type="number" dataKey="y" reversed hide />
        <ZAxis range={[20, 20]} />
        <Scatter data={data} fill={color} />
      </ScatterChart>
    </div>
  );
};

export default Chart;
