import React from 'react';
import { Link } from 'react-router-dom';
import { Calendar, User, Tag } from 'lucide-react';
import { getAppConfig } from '../config/appConfig';
import defaultImage from '../imgs/PDZ.jpg';

const ItemCard = ({ item }) => {
  const appConfig = getAppConfig();

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  };

  const renderMetaFields = () => {
    if (!item.meta_field || Object.keys(item.meta_field).length === 0) {
      return null;
    }

    return (
      <div className="mt-3 space-y-1">
        {appConfig.metaFields.slice(0, 2).map((field) => {
          const value = item.meta_field[field.name];
          if (!value) return null;

          return (
            <div key={field.name} className="flex items-center text-xs text-gray-500">
              <span className="font-medium mr-1">{field.label}:</span>
              <span>{field.type === 'boolean' ? (value ? 'Yes' : 'No') : value}</span>
            </div>
          );
        })}
      </div>
    );
  };

  const getImageSrc = () => {
    if (item.images && item.images.length > 0) {
      return item.images[0];
    }
    return defaultImage;
  };

  return (
    <div className="card card-hover">
      {/* Image */}
      <div className="aspect-w-16 aspect-h-9">
        <img
          src={getImageSrc()}
          alt={item.title}
          className="w-full h-48 object-cover"
          onError={(e) => {
            e.target.src = defaultImage;
          }}
        />
      </div>

      <div className="p-6">
        {/* Category */}
        <div className="flex items-center mb-2">
          <Tag className="w-4 h-4 mr-1 text-gray-400" />
          <span className={`text-xs font-medium ${appConfig.theme.accent}`}>
            {item.category}
          </span>
        </div>

        {/* Title */}
        <h3 className="text-lg font-semibold text-gray-900 mb-2 line-clamp-2">
          <Link
            to={`/items/${item.id}`}
            className="hover:text-gray-700 transition-colors duration-200"
          >
            {item.title}
          </Link>
        </h3>

        {/* Abstract */}
        <p className="text-gray-600 text-sm mb-4 line-clamp-3">
          {item.abstract}
        </p>

        {/* Meta fields */}
        {renderMetaFields()}

        {/* Tags */}
        {item.tags && item.tags.length > 0 && (
          <div className="mt-3 flex flex-wrap gap-1">
            {item.tags.slice(0, 3).map((tag, index) => (
              <span
                key={index}
                className="inline-block px-2 py-1 text-xs bg-gray-100 text-gray-600 rounded-full"
              >
                {tag}
              </span>
            ))}
            {item.tags.length > 3 && (
              <span className="inline-block px-2 py-1 text-xs text-gray-500">
                +{item.tags.length - 3} more
              </span>
            )}
          </div>
        )}

        {/* Footer */}
        <div className="mt-4 pt-4 border-t border-gray-100 flex items-center justify-between text-xs text-gray-500">
          <div className="flex items-center">
            <User className="w-4 h-4 mr-1" />
            <span>{item.author_name || `Author ${item.author_id?.slice(0, 8)}`}</span>
          </div>
          <div className="flex items-center">
            <Calendar className="w-4 h-4 mr-1" />
            <span>{formatDate(item.created_at || item.createdAt)}</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ItemCard;

