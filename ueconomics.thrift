////////////////////////////////////////////////////////////////////////////////////////////
//           /$$$$$$$$                                                 /$$
//          | $$_____/                                                |__/
//  /$$   /$| $$       /$$$$$$$ /$$$$$$ /$$$$$$$  /$$$$$$ /$$$$$$/$$$$ /$$ /$$$$$$$ /$$$$$$$
// | $$  | $| $$$$$   /$$_____//$$__  $| $$__  $$/$$__  $| $$_  $$_  $| $$/$$_____//$$_____/
// | $$  | $| $$__/  | $$     | $$  \ $| $$  \ $| $$  \ $| $$ \ $$ \ $| $| $$     |  $$$$$$
// | $$  | $| $$     | $$     | $$  | $| $$  | $| $$  | $| $$ | $$ | $| $| $$      \____  $$
// |  $$$$$$| $$$$$$$|  $$$$$$|  $$$$$$| $$  | $|  $$$$$$| $$ | $$ | $| $|  $$$$$$$/$$$$$$$/
//  \______/|________/\_______/\______/|__/  |__/\______/|__/ |__/ |__|__/\_______|_______/
////////////////////////////////////////////////////////////////////////////////////////////


namespace java com.uber.finance.ueconomics

////////////////////////////////////////////////////////////
// Exceptions
////////////////////////////////////////////////////////////

/**
 * Common exception for any uncaught exception
 */
exception InternalServerError {
  1: required string message;
}

/*
 * exception thrown when emailId is not present
 */
exception EmailIDNotFoundError{
    1: required string message;
}

/*
 * exception thrown when uuid is not present
 */
exception UUIDNotFoundError{
    1: required string message;
}

exception AccessError{
    1: required string message;
}

////////////////////////////////////////////////////////////
// Entities
////////////////////////////////////////////////////////////

struct HelloRequest {
    1: optional string name;
}

struct HelloResponse {
    1: optional string message;
}

struct Date{
  1: required i32 day
  2: required i32 month
  3: required i32 year
}

/**
 * EconomicsMetric specifies percentage comparison from past aggregationType
 * and value in given currency
 */
struct EconomicsMetric {
    1: required double percent,     // the percent change from past day/week/month
    2: required double value,        // metric value in given currency
}

enum ViewType{
   ACCOUNTING,
   OPERATIONAL,
}

enum AggregationType {
  DAILY,
  WEEKLY,
  MONTHLY,
  YEARLY,
}

enum CurrencyType{
  LOCAL,
  USD,
}

// DashboardType can be PNL or TripEconomics
enum DashboardType{
   PNL,
   TRIP_ECONOMICS,
}

// TODO: write API to get names of all the line items maintained by ueconomics
// for now, refer the json tags in model LedgerLineItems
struct TripEconomicsRequest {
    /**
     * e.g. OPERATIONAL, ACCOUNTING
     */
    1: required ViewType view,
    2: required Date startDate,
    /**
     * unique location identifier
     */
    3: required list<string> locationIdentifiers,
    4: optional Date endDate,
    5: optional list<string> linesOfBusiness,
    6: optional list<string> products,
    /**
     * e.g. USD or LOCAL
     */
    7: optional CurrencyType currency,
    /**
     * Week over Week, Daily or Monthly
     */
    8: optional AggregationType aggType,
    /**
     * Email ID for download request
     */
    9: optional string emailID,
    /**
     * User UUID
     */
    10: optional string uuid,
    /**
     * filter to choose line items needed in response
     */
    11: optional list<string> ledgerLineItems
    /**
     * dashboard - type defines corresponding views for trips and pnl
     */
    12: optional DashboardType dashboard // pnl or tripeconomics
    13: optional i64 (js.type = "Long") locationVersion
    14: required LocationHierarchyType locationHierarchyType
}

// TODO: if locationLevel is false return data for all locations,
// currently if locationLevel is false, it is mandatory to provide
// locationIdentifier list to filter on
/**
 * LineItemsRequest struct
 * can provide line items data at date x location x lob x product level
 */
struct LineItemsRequest {
    /**
     * e.g. OPERATIONAL, ACCOUNTING
     */
    1: required ViewType view,
    2: required Date startDate,
    /**
     * unique location identifier
     */
    3: optional list<string> locationIdentifiers,
    4: required Date endDate,
    /**
     * e.g. TNP, UFP, UberEATS
     */
    5: optional list<string> linesOfBusiness,
    /**
     * e.g. UberX Master, SUV Master
     */
    6: optional list<string> products,
    /**
     * filter to choose line items needed in response
     */
    7: optional list<string> ledgerLineItems
    /**
     * e.g. USD or LOCAL
     */
    8: optional CurrencyType currency,
    /**
     * Week over Week, Daily or Monthly
     */
    9: optional AggregationType aggType,
    10: optional bool lobLevel, // data will be returned lob wise
    11: optional bool locationLevel,
    12: optional bool productLevel
    13: optional i64 (js.type = "Long") locationVersion
    14: required LocationHierarchyType locationHierarchyType
}

/**
 * DateToFinancialMetrics is the struct with fields like date and its corresponding lineItems
 */
struct DateToFinancialMetrics{
    1: required string date,
    2: required map<string,EconomicsMetric> lineItems
}

/**
 * TripEconomicsResponse is list of DateToFinancialMetrics representing
 * line items for consecutive week / monthly
 */
struct TripEconomicsResponse {
    1: required list<DateToFinancialMetrics> metrics
    2: required bool newLocationVersionAvailable
    3: required i64 (js.type = "Long") locationVersion
}

/**
 * TripEconomicsForAllViews is an aggregated view of past few weeks / month
 * based on the aggregation type, and Month to Date and Year to date data
 */
 //TODO: create sub struct of TripEconomicsResponse without version details, and have outer struct return those fields
struct TripEconomicsForAllViews {
    // for each dashboardResponse type (i.e total/trip/percent) , we give its corresponding response
    1: required map<string, TripEconomicsResponse> dashboardResponse
}

/**
 * Node representing any location in hierarchy
 */
struct LocationNode {
    /**
     * Unique identifier
     */
    1:required i64 (js.type = "Long") id;
    /**
     * Name of the location
     */
    3:required string value;
    /**
     * Currency is USD and local
     */
    4:required string currency;
    /**
     * all location childs
     */
    5:optional list<LocationNode> buckets;
}

struct LocationForest {
    1: required list<LocationNode> locationHierarchyTrees;
    2: required i64 (js.type = "Long") version
}

// if req param 'LobLevel' is set to True, the field lob will have a single lob
// if LobLevel = false, reqLob = [l1, l2], then lob = [l1,l2]
// if LobLevel = false, reqLob = nil, then lob = nil
// TODO: modify the last case, to return list of all lobs instead of nil
// same follows for locationIdentifier and product
struct LineItemsResponse {
    1: required string date
    2: required map<string,double> lineItems
    3: optional list<string> lob
    4: optional list<string> locationIdentifiers
    5: optional list<string> product
}

enum LocationHierarchyType{
  RIDER =0,
  EATS,
}

struct DimensionNode{
    /**
     * Value of dimension
     */
    1:required string value;
    /**
     * All the children of DimensionNode
     */
    2:optional list<DimensionNode> buckets;
}

struct DimensionForest{
    1: required list<DimensionNode> dimensionTrees
}

enum DimensionType{
  LOB = 0
}

/**
 * UserAccessProfileResponse is the map of location hierarchies and dimension hierarchies
 * for each type of location and dimension
 */
struct UserAccessProfileResponse {
    1:required map<LocationHierarchyType, LocationForest> locationMap
    2:required map<DimensionType, DimensionForest> dimensionMap
}

////////////////////////////////////////////////////////////
// Services
////////////////////////////////////////////////////////////

service Ueconomics {

  /**
   * GetTripEconomics : gives trip economics on total basis
   */
  TripEconomicsResponse getTripEconomics(
      1: TripEconomicsRequest tripEconomicsRequest
  ) throws (
      1: InternalServerError serverError,
  ) (cerberus.enabled = "true", cerberus.type = "read")

  /**
   * GetTripEconomicsPerTrip : gives trip economics on trip basis
   */
  TripEconomicsResponse getTripEconomicsPerTrip(
      1: TripEconomicsRequest tripEconomicsRequest
  ) throws (
      1: InternalServerError serverError,
  ) (cerberus.enabled = "true", cerberus.type = "read")

  /**
   * Gives trip economics on percentage basis
   */
  TripEconomicsResponse getTripEconomicsPerPercentage(
      1: TripEconomicsRequest tripEconomicsRequest
  ) throws (
      1: InternalServerError serverError,
  ) (cerberus.enabled = "true", cerberus.type = "read")

  /**
   * Gives all financial metrics based on aggType (weekly/monthly)
   * and overall YTD , MTD and previous Month view for all dashboards trip/total/percent
   */
  TripEconomicsForAllViews getMetricsForTripEconomics(1: TripEconomicsRequest
                tripEconomicsRequest
  ) throws (
      1: InternalServerError serverError,
  ) (cerberus.enabled = "true", cerberus.type = "read")

  /**
   * getUserAccessProfile shall fetch the hierarchies for location and dimension types
   */
  UserAccessProfileResponse  getUserAccessProfile(
      1: string userid
  )
  throws (
      1: AccessError accessError,
      2: InternalServerError serverError,
  ) (cerberus.enabled = "true", cerberus.type = "read")

  /**
   * Provides only the required line items
   */
  //TODO: make it contain in struct and add locationVersion
  list<LineItemsResponse> getLineItems(
      1: LineItemsRequest lineItemsRequest
  ) throws (
      1: InternalServerError serverError,
  ) (cerberus.enabled = "true", cerberus.type = "read")

  /**
   * Processes download requests from UI and sends the email for given EmailID
   */
  void processEmailRequest(
      1: TripEconomicsRequest tripEconomicsRequest
   ) throws (
      1: EmailIDNotFoundError emailError,
      2: InternalServerError serverError,
  )(cerberus.enabled = "true", cerberus.type = "read")
}
