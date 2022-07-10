// Generated by the protocol buffer compiler.  DO NOT EDIT!
// source: partner_api.proto

package com.emporiaenergy.protos.partnerapi;

/**
 * Protobuf type {@code protos.AuthenticationResponse}
 */
public final class AuthenticationResponse extends
    com.google.protobuf.GeneratedMessageV3 implements
    // @@protoc_insertion_point(message_implements:protos.AuthenticationResponse)
    AuthenticationResponseOrBuilder {
private static final long serialVersionUID = 0L;
  // Use AuthenticationResponse.newBuilder() to construct.
  private AuthenticationResponse(com.google.protobuf.GeneratedMessageV3.Builder<?> builder) {
    super(builder);
  }
  private AuthenticationResponse() {
    authToken_ = "";
    resultStatus_ = 0;
  }

  @java.lang.Override
  @SuppressWarnings({"unused"})
  protected java.lang.Object newInstance(
      UnusedPrivateParameter unused) {
    return new AuthenticationResponse();
  }

  @java.lang.Override
  public final com.google.protobuf.UnknownFieldSet
  getUnknownFields() {
    return this.unknownFields;
  }
  private AuthenticationResponse(
      com.google.protobuf.CodedInputStream input,
      com.google.protobuf.ExtensionRegistryLite extensionRegistry)
      throws com.google.protobuf.InvalidProtocolBufferException {
    this();
    if (extensionRegistry == null) {
      throw new java.lang.NullPointerException();
    }
    com.google.protobuf.UnknownFieldSet.Builder unknownFields =
        com.google.protobuf.UnknownFieldSet.newBuilder();
    try {
      boolean done = false;
      while (!done) {
        int tag = input.readTag();
        switch (tag) {
          case 0:
            done = true;
            break;
          case 10: {
            java.lang.String s = input.readStringRequireUtf8();

            authToken_ = s;
            break;
          }
          case 800: {
            int rawValue = input.readEnum();

            resultStatus_ = rawValue;
            break;
          }
          default: {
            if (!parseUnknownField(
                input, unknownFields, extensionRegistry, tag)) {
              done = true;
            }
            break;
          }
        }
      }
    } catch (com.google.protobuf.InvalidProtocolBufferException e) {
      throw e.setUnfinishedMessage(this);
    } catch (java.io.IOException e) {
      throw new com.google.protobuf.InvalidProtocolBufferException(
          e).setUnfinishedMessage(this);
    } finally {
      this.unknownFields = unknownFields.build();
      makeExtensionsImmutable();
    }
  }
  public static final com.google.protobuf.Descriptors.Descriptor
      getDescriptor() {
    return com.emporiaenergy.protos.partnerapi.PartnerApiProto.internal_static_protos_AuthenticationResponse_descriptor;
  }

  @java.lang.Override
  protected com.google.protobuf.GeneratedMessageV3.FieldAccessorTable
      internalGetFieldAccessorTable() {
    return com.emporiaenergy.protos.partnerapi.PartnerApiProto.internal_static_protos_AuthenticationResponse_fieldAccessorTable
        .ensureFieldAccessorsInitialized(
            com.emporiaenergy.protos.partnerapi.AuthenticationResponse.class, com.emporiaenergy.protos.partnerapi.AuthenticationResponse.Builder.class);
  }

  public static final int AUTH_TOKEN_FIELD_NUMBER = 1;
  private volatile java.lang.Object authToken_;
  /**
   * <code>string auth_token = 1;</code>
   * @return The authToken.
   */
  @java.lang.Override
  public java.lang.String getAuthToken() {
    java.lang.Object ref = authToken_;
    if (ref instanceof java.lang.String) {
      return (java.lang.String) ref;
    } else {
      com.google.protobuf.ByteString bs = 
          (com.google.protobuf.ByteString) ref;
      java.lang.String s = bs.toStringUtf8();
      authToken_ = s;
      return s;
    }
  }
  /**
   * <code>string auth_token = 1;</code>
   * @return The bytes for authToken.
   */
  @java.lang.Override
  public com.google.protobuf.ByteString
      getAuthTokenBytes() {
    java.lang.Object ref = authToken_;
    if (ref instanceof java.lang.String) {
      com.google.protobuf.ByteString b = 
          com.google.protobuf.ByteString.copyFromUtf8(
              (java.lang.String) ref);
      authToken_ = b;
      return b;
    } else {
      return (com.google.protobuf.ByteString) ref;
    }
  }

  public static final int RESULT_STATUS_FIELD_NUMBER = 100;
  private int resultStatus_;
  /**
   * <code>.protos.ResultStatus result_status = 100;</code>
   * @return The enum numeric value on the wire for resultStatus.
   */
  @java.lang.Override public int getResultStatusValue() {
    return resultStatus_;
  }
  /**
   * <code>.protos.ResultStatus result_status = 100;</code>
   * @return The resultStatus.
   */
  @java.lang.Override public com.emporiaenergy.protos.partnerapi.ResultStatus getResultStatus() {
    @SuppressWarnings("deprecation")
    com.emporiaenergy.protos.partnerapi.ResultStatus result = com.emporiaenergy.protos.partnerapi.ResultStatus.valueOf(resultStatus_);
    return result == null ? com.emporiaenergy.protos.partnerapi.ResultStatus.UNRECOGNIZED : result;
  }

  private byte memoizedIsInitialized = -1;
  @java.lang.Override
  public final boolean isInitialized() {
    byte isInitialized = memoizedIsInitialized;
    if (isInitialized == 1) return true;
    if (isInitialized == 0) return false;

    memoizedIsInitialized = 1;
    return true;
  }

  @java.lang.Override
  public void writeTo(com.google.protobuf.CodedOutputStream output)
                      throws java.io.IOException {
    if (!getAuthTokenBytes().isEmpty()) {
      com.google.protobuf.GeneratedMessageV3.writeString(output, 1, authToken_);
    }
    if (resultStatus_ != com.emporiaenergy.protos.partnerapi.ResultStatus.VALID.getNumber()) {
      output.writeEnum(100, resultStatus_);
    }
    unknownFields.writeTo(output);
  }

  @java.lang.Override
  public int getSerializedSize() {
    int size = memoizedSize;
    if (size != -1) return size;

    size = 0;
    if (!getAuthTokenBytes().isEmpty()) {
      size += com.google.protobuf.GeneratedMessageV3.computeStringSize(1, authToken_);
    }
    if (resultStatus_ != com.emporiaenergy.protos.partnerapi.ResultStatus.VALID.getNumber()) {
      size += com.google.protobuf.CodedOutputStream
        .computeEnumSize(100, resultStatus_);
    }
    size += unknownFields.getSerializedSize();
    memoizedSize = size;
    return size;
  }

  @java.lang.Override
  public boolean equals(final java.lang.Object obj) {
    if (obj == this) {
     return true;
    }
    if (!(obj instanceof com.emporiaenergy.protos.partnerapi.AuthenticationResponse)) {
      return super.equals(obj);
    }
    com.emporiaenergy.protos.partnerapi.AuthenticationResponse other = (com.emporiaenergy.protos.partnerapi.AuthenticationResponse) obj;

    if (!getAuthToken()
        .equals(other.getAuthToken())) return false;
    if (resultStatus_ != other.resultStatus_) return false;
    if (!unknownFields.equals(other.unknownFields)) return false;
    return true;
  }

  @java.lang.Override
  public int hashCode() {
    if (memoizedHashCode != 0) {
      return memoizedHashCode;
    }
    int hash = 41;
    hash = (19 * hash) + getDescriptor().hashCode();
    hash = (37 * hash) + AUTH_TOKEN_FIELD_NUMBER;
    hash = (53 * hash) + getAuthToken().hashCode();
    hash = (37 * hash) + RESULT_STATUS_FIELD_NUMBER;
    hash = (53 * hash) + resultStatus_;
    hash = (29 * hash) + unknownFields.hashCode();
    memoizedHashCode = hash;
    return hash;
  }

  public static com.emporiaenergy.protos.partnerapi.AuthenticationResponse parseFrom(
      java.nio.ByteBuffer data)
      throws com.google.protobuf.InvalidProtocolBufferException {
    return PARSER.parseFrom(data);
  }
  public static com.emporiaenergy.protos.partnerapi.AuthenticationResponse parseFrom(
      java.nio.ByteBuffer data,
      com.google.protobuf.ExtensionRegistryLite extensionRegistry)
      throws com.google.protobuf.InvalidProtocolBufferException {
    return PARSER.parseFrom(data, extensionRegistry);
  }
  public static com.emporiaenergy.protos.partnerapi.AuthenticationResponse parseFrom(
      com.google.protobuf.ByteString data)
      throws com.google.protobuf.InvalidProtocolBufferException {
    return PARSER.parseFrom(data);
  }
  public static com.emporiaenergy.protos.partnerapi.AuthenticationResponse parseFrom(
      com.google.protobuf.ByteString data,
      com.google.protobuf.ExtensionRegistryLite extensionRegistry)
      throws com.google.protobuf.InvalidProtocolBufferException {
    return PARSER.parseFrom(data, extensionRegistry);
  }
  public static com.emporiaenergy.protos.partnerapi.AuthenticationResponse parseFrom(byte[] data)
      throws com.google.protobuf.InvalidProtocolBufferException {
    return PARSER.parseFrom(data);
  }
  public static com.emporiaenergy.protos.partnerapi.AuthenticationResponse parseFrom(
      byte[] data,
      com.google.protobuf.ExtensionRegistryLite extensionRegistry)
      throws com.google.protobuf.InvalidProtocolBufferException {
    return PARSER.parseFrom(data, extensionRegistry);
  }
  public static com.emporiaenergy.protos.partnerapi.AuthenticationResponse parseFrom(java.io.InputStream input)
      throws java.io.IOException {
    return com.google.protobuf.GeneratedMessageV3
        .parseWithIOException(PARSER, input);
  }
  public static com.emporiaenergy.protos.partnerapi.AuthenticationResponse parseFrom(
      java.io.InputStream input,
      com.google.protobuf.ExtensionRegistryLite extensionRegistry)
      throws java.io.IOException {
    return com.google.protobuf.GeneratedMessageV3
        .parseWithIOException(PARSER, input, extensionRegistry);
  }
  public static com.emporiaenergy.protos.partnerapi.AuthenticationResponse parseDelimitedFrom(java.io.InputStream input)
      throws java.io.IOException {
    return com.google.protobuf.GeneratedMessageV3
        .parseDelimitedWithIOException(PARSER, input);
  }
  public static com.emporiaenergy.protos.partnerapi.AuthenticationResponse parseDelimitedFrom(
      java.io.InputStream input,
      com.google.protobuf.ExtensionRegistryLite extensionRegistry)
      throws java.io.IOException {
    return com.google.protobuf.GeneratedMessageV3
        .parseDelimitedWithIOException(PARSER, input, extensionRegistry);
  }
  public static com.emporiaenergy.protos.partnerapi.AuthenticationResponse parseFrom(
      com.google.protobuf.CodedInputStream input)
      throws java.io.IOException {
    return com.google.protobuf.GeneratedMessageV3
        .parseWithIOException(PARSER, input);
  }
  public static com.emporiaenergy.protos.partnerapi.AuthenticationResponse parseFrom(
      com.google.protobuf.CodedInputStream input,
      com.google.protobuf.ExtensionRegistryLite extensionRegistry)
      throws java.io.IOException {
    return com.google.protobuf.GeneratedMessageV3
        .parseWithIOException(PARSER, input, extensionRegistry);
  }

  @java.lang.Override
  public Builder newBuilderForType() { return newBuilder(); }
  public static Builder newBuilder() {
    return DEFAULT_INSTANCE.toBuilder();
  }
  public static Builder newBuilder(com.emporiaenergy.protos.partnerapi.AuthenticationResponse prototype) {
    return DEFAULT_INSTANCE.toBuilder().mergeFrom(prototype);
  }
  @java.lang.Override
  public Builder toBuilder() {
    return this == DEFAULT_INSTANCE
        ? new Builder() : new Builder().mergeFrom(this);
  }

  @java.lang.Override
  protected Builder newBuilderForType(
      com.google.protobuf.GeneratedMessageV3.BuilderParent parent) {
    Builder builder = new Builder(parent);
    return builder;
  }
  /**
   * Protobuf type {@code protos.AuthenticationResponse}
   */
  public static final class Builder extends
      com.google.protobuf.GeneratedMessageV3.Builder<Builder> implements
      // @@protoc_insertion_point(builder_implements:protos.AuthenticationResponse)
      com.emporiaenergy.protos.partnerapi.AuthenticationResponseOrBuilder {
    public static final com.google.protobuf.Descriptors.Descriptor
        getDescriptor() {
      return com.emporiaenergy.protos.partnerapi.PartnerApiProto.internal_static_protos_AuthenticationResponse_descriptor;
    }

    @java.lang.Override
    protected com.google.protobuf.GeneratedMessageV3.FieldAccessorTable
        internalGetFieldAccessorTable() {
      return com.emporiaenergy.protos.partnerapi.PartnerApiProto.internal_static_protos_AuthenticationResponse_fieldAccessorTable
          .ensureFieldAccessorsInitialized(
              com.emporiaenergy.protos.partnerapi.AuthenticationResponse.class, com.emporiaenergy.protos.partnerapi.AuthenticationResponse.Builder.class);
    }

    // Construct using com.emporiaenergy.protos.partnerapi.AuthenticationResponse.newBuilder()
    private Builder() {
      maybeForceBuilderInitialization();
    }

    private Builder(
        com.google.protobuf.GeneratedMessageV3.BuilderParent parent) {
      super(parent);
      maybeForceBuilderInitialization();
    }
    private void maybeForceBuilderInitialization() {
      if (com.google.protobuf.GeneratedMessageV3
              .alwaysUseFieldBuilders) {
      }
    }
    @java.lang.Override
    public Builder clear() {
      super.clear();
      authToken_ = "";

      resultStatus_ = 0;

      return this;
    }

    @java.lang.Override
    public com.google.protobuf.Descriptors.Descriptor
        getDescriptorForType() {
      return com.emporiaenergy.protos.partnerapi.PartnerApiProto.internal_static_protos_AuthenticationResponse_descriptor;
    }

    @java.lang.Override
    public com.emporiaenergy.protos.partnerapi.AuthenticationResponse getDefaultInstanceForType() {
      return com.emporiaenergy.protos.partnerapi.AuthenticationResponse.getDefaultInstance();
    }

    @java.lang.Override
    public com.emporiaenergy.protos.partnerapi.AuthenticationResponse build() {
      com.emporiaenergy.protos.partnerapi.AuthenticationResponse result = buildPartial();
      if (!result.isInitialized()) {
        throw newUninitializedMessageException(result);
      }
      return result;
    }

    @java.lang.Override
    public com.emporiaenergy.protos.partnerapi.AuthenticationResponse buildPartial() {
      com.emporiaenergy.protos.partnerapi.AuthenticationResponse result = new com.emporiaenergy.protos.partnerapi.AuthenticationResponse(this);
      result.authToken_ = authToken_;
      result.resultStatus_ = resultStatus_;
      onBuilt();
      return result;
    }

    @java.lang.Override
    public Builder clone() {
      return super.clone();
    }
    @java.lang.Override
    public Builder setField(
        com.google.protobuf.Descriptors.FieldDescriptor field,
        java.lang.Object value) {
      return super.setField(field, value);
    }
    @java.lang.Override
    public Builder clearField(
        com.google.protobuf.Descriptors.FieldDescriptor field) {
      return super.clearField(field);
    }
    @java.lang.Override
    public Builder clearOneof(
        com.google.protobuf.Descriptors.OneofDescriptor oneof) {
      return super.clearOneof(oneof);
    }
    @java.lang.Override
    public Builder setRepeatedField(
        com.google.protobuf.Descriptors.FieldDescriptor field,
        int index, java.lang.Object value) {
      return super.setRepeatedField(field, index, value);
    }
    @java.lang.Override
    public Builder addRepeatedField(
        com.google.protobuf.Descriptors.FieldDescriptor field,
        java.lang.Object value) {
      return super.addRepeatedField(field, value);
    }
    @java.lang.Override
    public Builder mergeFrom(com.google.protobuf.Message other) {
      if (other instanceof com.emporiaenergy.protos.partnerapi.AuthenticationResponse) {
        return mergeFrom((com.emporiaenergy.protos.partnerapi.AuthenticationResponse)other);
      } else {
        super.mergeFrom(other);
        return this;
      }
    }

    public Builder mergeFrom(com.emporiaenergy.protos.partnerapi.AuthenticationResponse other) {
      if (other == com.emporiaenergy.protos.partnerapi.AuthenticationResponse.getDefaultInstance()) return this;
      if (!other.getAuthToken().isEmpty()) {
        authToken_ = other.authToken_;
        onChanged();
      }
      if (other.resultStatus_ != 0) {
        setResultStatusValue(other.getResultStatusValue());
      }
      this.mergeUnknownFields(other.unknownFields);
      onChanged();
      return this;
    }

    @java.lang.Override
    public final boolean isInitialized() {
      return true;
    }

    @java.lang.Override
    public Builder mergeFrom(
        com.google.protobuf.CodedInputStream input,
        com.google.protobuf.ExtensionRegistryLite extensionRegistry)
        throws java.io.IOException {
      com.emporiaenergy.protos.partnerapi.AuthenticationResponse parsedMessage = null;
      try {
        parsedMessage = PARSER.parsePartialFrom(input, extensionRegistry);
      } catch (com.google.protobuf.InvalidProtocolBufferException e) {
        parsedMessage = (com.emporiaenergy.protos.partnerapi.AuthenticationResponse) e.getUnfinishedMessage();
        throw e.unwrapIOException();
      } finally {
        if (parsedMessage != null) {
          mergeFrom(parsedMessage);
        }
      }
      return this;
    }

    private java.lang.Object authToken_ = "";
    /**
     * <code>string auth_token = 1;</code>
     * @return The authToken.
     */
    public java.lang.String getAuthToken() {
      java.lang.Object ref = authToken_;
      if (!(ref instanceof java.lang.String)) {
        com.google.protobuf.ByteString bs =
            (com.google.protobuf.ByteString) ref;
        java.lang.String s = bs.toStringUtf8();
        authToken_ = s;
        return s;
      } else {
        return (java.lang.String) ref;
      }
    }
    /**
     * <code>string auth_token = 1;</code>
     * @return The bytes for authToken.
     */
    public com.google.protobuf.ByteString
        getAuthTokenBytes() {
      java.lang.Object ref = authToken_;
      if (ref instanceof String) {
        com.google.protobuf.ByteString b = 
            com.google.protobuf.ByteString.copyFromUtf8(
                (java.lang.String) ref);
        authToken_ = b;
        return b;
      } else {
        return (com.google.protobuf.ByteString) ref;
      }
    }
    /**
     * <code>string auth_token = 1;</code>
     * @param value The authToken to set.
     * @return This builder for chaining.
     */
    public Builder setAuthToken(
        java.lang.String value) {
      if (value == null) {
    throw new NullPointerException();
  }
  
      authToken_ = value;
      onChanged();
      return this;
    }
    /**
     * <code>string auth_token = 1;</code>
     * @return This builder for chaining.
     */
    public Builder clearAuthToken() {
      
      authToken_ = getDefaultInstance().getAuthToken();
      onChanged();
      return this;
    }
    /**
     * <code>string auth_token = 1;</code>
     * @param value The bytes for authToken to set.
     * @return This builder for chaining.
     */
    public Builder setAuthTokenBytes(
        com.google.protobuf.ByteString value) {
      if (value == null) {
    throw new NullPointerException();
  }
  checkByteStringIsUtf8(value);
      
      authToken_ = value;
      onChanged();
      return this;
    }

    private int resultStatus_ = 0;
    /**
     * <code>.protos.ResultStatus result_status = 100;</code>
     * @return The enum numeric value on the wire for resultStatus.
     */
    @java.lang.Override public int getResultStatusValue() {
      return resultStatus_;
    }
    /**
     * <code>.protos.ResultStatus result_status = 100;</code>
     * @param value The enum numeric value on the wire for resultStatus to set.
     * @return This builder for chaining.
     */
    public Builder setResultStatusValue(int value) {
      
      resultStatus_ = value;
      onChanged();
      return this;
    }
    /**
     * <code>.protos.ResultStatus result_status = 100;</code>
     * @return The resultStatus.
     */
    @java.lang.Override
    public com.emporiaenergy.protos.partnerapi.ResultStatus getResultStatus() {
      @SuppressWarnings("deprecation")
      com.emporiaenergy.protos.partnerapi.ResultStatus result = com.emporiaenergy.protos.partnerapi.ResultStatus.valueOf(resultStatus_);
      return result == null ? com.emporiaenergy.protos.partnerapi.ResultStatus.UNRECOGNIZED : result;
    }
    /**
     * <code>.protos.ResultStatus result_status = 100;</code>
     * @param value The resultStatus to set.
     * @return This builder for chaining.
     */
    public Builder setResultStatus(com.emporiaenergy.protos.partnerapi.ResultStatus value) {
      if (value == null) {
        throw new NullPointerException();
      }
      
      resultStatus_ = value.getNumber();
      onChanged();
      return this;
    }
    /**
     * <code>.protos.ResultStatus result_status = 100;</code>
     * @return This builder for chaining.
     */
    public Builder clearResultStatus() {
      
      resultStatus_ = 0;
      onChanged();
      return this;
    }
    @java.lang.Override
    public final Builder setUnknownFields(
        final com.google.protobuf.UnknownFieldSet unknownFields) {
      return super.setUnknownFields(unknownFields);
    }

    @java.lang.Override
    public final Builder mergeUnknownFields(
        final com.google.protobuf.UnknownFieldSet unknownFields) {
      return super.mergeUnknownFields(unknownFields);
    }


    // @@protoc_insertion_point(builder_scope:protos.AuthenticationResponse)
  }

  // @@protoc_insertion_point(class_scope:protos.AuthenticationResponse)
  private static final com.emporiaenergy.protos.partnerapi.AuthenticationResponse DEFAULT_INSTANCE;
  static {
    DEFAULT_INSTANCE = new com.emporiaenergy.protos.partnerapi.AuthenticationResponse();
  }

  public static com.emporiaenergy.protos.partnerapi.AuthenticationResponse getDefaultInstance() {
    return DEFAULT_INSTANCE;
  }

  private static final com.google.protobuf.Parser<AuthenticationResponse>
      PARSER = new com.google.protobuf.AbstractParser<AuthenticationResponse>() {
    @java.lang.Override
    public AuthenticationResponse parsePartialFrom(
        com.google.protobuf.CodedInputStream input,
        com.google.protobuf.ExtensionRegistryLite extensionRegistry)
        throws com.google.protobuf.InvalidProtocolBufferException {
      return new AuthenticationResponse(input, extensionRegistry);
    }
  };

  public static com.google.protobuf.Parser<AuthenticationResponse> parser() {
    return PARSER;
  }

  @java.lang.Override
  public com.google.protobuf.Parser<AuthenticationResponse> getParserForType() {
    return PARSER;
  }

  @java.lang.Override
  public com.emporiaenergy.protos.partnerapi.AuthenticationResponse getDefaultInstanceForType() {
    return DEFAULT_INSTANCE;
  }

}

