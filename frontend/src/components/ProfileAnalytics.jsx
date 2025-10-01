import React from 'react';
import { BarChart3, TrendingUp, Eye, Users, Calendar, Award } from 'lucide-react';

const ProfileAnalytics = ({ userItems, user }) => {
  // Calculate some basic analytics
  const totalViews = userItems.reduce((sum, item) => sum + (item.views || 0), 0);
  const totalLikes = userItems.reduce((sum, item) => sum + (item.likes || 0), 0);
  const publishedItems = userItems.filter(item => item.status === 'published').length;
  const draftItems = userItems.filter(item => item.status === 'draft').length;
  
  // Calculate this month's items
  const thisMonth = new Date();
  thisMonth.setDate(1);
  const thisMonthItems = userItems.filter(item => {
    const itemDate = new Date(item.created_at || item.createdAt);
    return itemDate >= thisMonth;
  }).length;

  // Calculate average views per item
  const avgViews = publishedItems > 0 ? Math.round(totalViews / publishedItems) : 0;

  const stats = [
    {
      name: 'Total Items',
      value: userItems.length,
      change: `+${thisMonthItems} this month`,
      changeType: 'positive',
      icon: BarChart3,
      color: 'bg-blue-500',
    },
    {
      name: 'Published',
      value: publishedItems,
      change: `${draftItems} drafts`,
      changeType: 'neutral',
      icon: Award,
      color: 'bg-green-500',
    },
    {
      name: 'Total Views',
      value: totalViews.toLocaleString(),
      change: `${avgViews} avg per article`,
      changeType: 'positive',
      icon: Eye,
      color: 'bg-purple-500',
    },
    {
      name: 'Engagement',
      value: totalLikes.toLocaleString(),
      change: 'Total likes received',
      changeType: 'positive',
      icon: Users,
      color: 'bg-pink-500',
    },
  ];

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-8">
      <div className="flex items-center mb-6">
        <TrendingUp className="w-6 h-6 text-blue-600 mr-3" />
        <h2 className="text-xl font-semibold text-gray-900">Analytics Overview</h2>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {stats.map((stat) => {
          const Icon = stat.icon;
          return (
            <div key={stat.name} className="bg-gray-50 rounded-lg p-4">
              <div className="flex items-center">
                <div className={`p-2 rounded-lg ${stat.color}`}>
                  <Icon className="w-5 h-5 text-white" />
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-600">{stat.name}</p>
                  <p className="text-2xl font-semibold text-gray-900">{stat.value}</p>
                </div>
              </div>
              <div className="mt-2">
                <p className={`text-sm ${
                  stat.changeType === 'positive' ? 'text-green-600' :
                  stat.changeType === 'negative' ? 'text-red-600' : 'text-gray-500'
                }`}>
                  {stat.change}
                </p>
              </div>
            </div>
          );
        })}
      </div>

      {/* Recent Activity Chart Placeholder */}
      <div className="mt-8 border-t border-gray-200 pt-6">
        <h3 className="text-lg font-medium text-gray-900 mb-4">Publishing Activity</h3>
        <div className="bg-gray-50 rounded-lg p-8 text-center">
          <Calendar className="w-12 h-12 text-gray-400 mx-auto mb-3" />
          <p className="text-gray-500">Activity chart coming soon</p>
          <p className="text-sm text-gray-400 mt-1">Track your publishing patterns over time</p>
        </div>
      </div>
    </div>
  );
};

export default ProfileAnalytics;
