# Django QuerySet Statistical Operations Guide

## Basic QuerySet Operations

**Flattening Lists**
```python
# Get a flat list of values for a specific term
queryset.values_list(term_to_be_find, flat=True).order_by(term_...)
```

## Vote Counting Operations

**Basic Vote Count**
```python
# Get vote count per choice in a poll
poll = get_object_or_404(Poll, poll_id)
Vote.objects.filter(poll=poll).values('choice').annotate(count=Count('choice'))

# Get vote count with choice text
votes = Vote.objects.values('choice__text').filter(poll=poll).annotate(count=Count('choice'))
```

## Statistical Calculations

**Mean Calculation**
```python
# Calculate average votes
mean = votes.aggregate(average=Avg('count'))
# Access mean value through mean['average']
```

**Median Calculation**
```python
def median_value(queryset, term):
    count = queryset.count()
    values = queryset.values_list(term, flat=True).order_by(term)
    if count % 2 == 1:
        return values[int(round(count/2))]
    else:
        return sum(values[count//2-1:count//2+1])/2.0

# Usage
median = median_value(votes, 'count')
```

**Mode Calculation**
```python
# Get mode count
mode_count = max(votes, key=lambda x: x['count'])['count']
# Get mode choice text
mode_text = max(votes, key=lambda x: x['count'])['choice__text']
```

**Variance and Standard Deviation**
```python
import statistics

# Get flat list of counts
data = votes.values_list('count', flat=True)

# Variance calculations
population_variance = statistics.pvariance(data, mean['average'])
sample_variance = statistics.variance(data, mean['average'])

# Standard deviation calculations
population_stddev = statistics.pstdev(data, mean['average'])
sample_stddev = statistics.stdev(data, mean['average'])
```

## Notes
- Use `flat=True` in `values_list()` to get a flat list instead of tuples
- For statistical calculations, consider whether you need population or sample statistics
- Always handle the case where the queryset might be empty
- The mode calculation assumes there is at least one vote in the dataset