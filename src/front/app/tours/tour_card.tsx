import React from "react";
import "./tour_card.css";
import airplane from "../../public/airplane.png";

interface TourCardProps {
  title: string;
  startDate: string;
  endDate: string;
  description: string;
}
// eslint-disable-next-line
const TourCard: React.FC<TourCardProps> = ({ title, startDate, endDate, description }) => {
  const formattedStartDate = formatDate(startDate);
  const formattedEndDate = formatDate(endDate);

  return (
      <div className="tour-card">
        <div className="tour-card__badge">
          <h2 className="tour-card__title">{title}</h2>
          <p className="tour-card__date">{`${formattedStartDate} - ${formattedEndDate}`}</p>
        </div>
        <img src={airplane.src} alt="Airplane" className="tour-card__image"/>
      </div>
  );
};

function formatDate(date: string): string {
  const options: Intl.DateTimeFormatOptions = { day: '2-digit', month: '2-digit', year: 'numeric' };
  return new Date(date).toLocaleDateString('ru-RU', options);
}

export default TourCard;